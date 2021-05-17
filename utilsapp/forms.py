from django import forms

from utilsapp.models import File


class FilesForm(forms.Form):
    is_deposit = forms.BooleanField(initial=True, required=False)
    psp_file = forms.FileField()
    db_file = forms.FileField()