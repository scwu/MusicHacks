from django import forms
from hacks.app.models import Genre

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), empty_label="(Nothing)")
    file = forms.FileField()
