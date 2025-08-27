from django import forms

class VideoDownloadForm(forms.Form):
    url = forms.URLField(
        label="Video URL",
        widget=forms.URLInput(attrs={
            "placeholder": "Enter video URL",
            "style": "width: 300px; padding: 5px"
        })
    )
