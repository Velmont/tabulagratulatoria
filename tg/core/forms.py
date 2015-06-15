from django.forms import ModelForm

from .models import Entry


class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = (
            'status', 'shown_name', 'first_name', 'last_name',
            'email', 'phone', 'address', 'postnummer', 'place',
            'notes', 'groups')
