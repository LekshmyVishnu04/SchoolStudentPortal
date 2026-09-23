from django import forms
from .models import Student


class StudentModelForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'cl']
        labels = {'name': 'Studnet Name', 'age': 'Age', 'cl': 'Class'}
