from django import forms
from hacks.app.models import Genre

class UploadFileForm(forms.Form):
    file = forms.FileField()
