from django import forms

from .models import Entry


class EntryForm(forms.ModelForm):
    want_tg = forms.BooleanField(initial=True, required=False)
    alt_address = forms.CharField(
        required=False, widget=forms.widgets.Textarea)

    class Meta:
        model = Entry
        fields = (
            'want_tg', 'num_issues',
            'shown_name', 'first_name', 'last_name',
            'email', 'phone', 'address', 'postnummer', 'place',
            )
