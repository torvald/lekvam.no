from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('text', 'image' ,'listid', 'due')
        labels = {
            "text": "Tekst",
            "image": "Bilde",
            "listid": "Bilde",
            "due": "Tidsfrist",
        }
