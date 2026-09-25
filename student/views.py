from django.shortcuts import render, redirect
from .models import Student
from .forms import StudentModelForm
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse

# Create your views here.


def home(request):
    search = request.GET.get('search')
    if search:
        data = Student.objects.filter(name__icontains=search)
    else:
        data = Student.objects.all()
    return render(request, 'home.html', {'data': data})


def add(request):
    if request.method == 'POST':
        form = StudentModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentModelForm()
    return render(request, 'add.html', {'form': form})


def edit(request, id):
    data = Student.objects.get(pk=id)
    if request.method == 'POST':
        form = StudentModelForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentModelForm(instance=data)
    return render(request, 'edit.html', {'form': form})


def delete(request, id):
    data = Student.objects.get(pk=id)
    if request.method == 'POST':
        data.delete()
        return redirect('home')
    return render(request, 'delete.html', {'data': data})


def download(request, id):
    data = get_object_or_404(Student, pk=id)
    template = get_template('student_pdf.html')
    html = template.render({'student': data})

    buffer = BytesIO()

    pisa_status = pisa.CreatePDF(html, dest=buffer)

    if pisa_status.err:
        return HttpResponse('PDF creation error!')
    else:
        response = HttpResponse(
            buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(
            data.name)
        return response
