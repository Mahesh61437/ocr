from django import forms


class UploadForm(forms.Form):
    image = forms.ImageField(label='Upload image', required=False)
    url = forms.CharField(required=False)


class DownloadForm(forms.Form):
    output = forms.CharField(widget=forms.Textarea)
