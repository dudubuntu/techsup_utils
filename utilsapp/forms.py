from django import forms

from utilsapp.models import File


class FilesForm(forms.Form):
    check_type = forms.CharField(max_length=20)
    psp_file = forms.FileField()
    db_file = forms.FileField()