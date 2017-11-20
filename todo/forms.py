from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('text', 'image' ,'listid')
        labels = {
            "text": "Tekst",
            "image": "Bilde",
            "listid": "Bilde",
        }
