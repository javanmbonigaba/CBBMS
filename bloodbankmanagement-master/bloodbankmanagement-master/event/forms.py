from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'venue', 'time']
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
