from django import forms


class EntryForm(forms.Form):
    want_tg = forms.BooleanField(initial=True, required=False)
    num_issues = forms.IntegerField(required=True, min_value=1,
                                    max_value=99)
    first_name = forms.CharField()
    last_name = forms.CharField()
    shown_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    full_address = forms.CharField(
        required=True, widget=forms.widgets.Textarea)
    other = forms.CharField(
        required=False, widget=forms.widgets.Textarea())
