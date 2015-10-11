import json

from django.core.mail import mail_managers
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from core.forms import EntryForm


def home(request):
    return render(request, 'ui/home.html', {})


def adder(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            text = _make_email_body(form.cleaned_data, request.META)
            mail_managers(form.cleaned_data.get('first_name', '(utan namn)'),
                          text)
            return HttpResponseRedirect(reverse('ui:takk'))
    else:
        form = EntryForm(initial={
            'want_issue': True,
            'want_tg': True,
            'num_issues': 1,
        })
    return render(request, 'ui/adder.html',
                  {
                      'form': form,
                  })


def _make_email_body(data, meta):
    text = ""
    for k in sorted(data.keys()):
        text += "{k}\n{v}\n\n".format(k=k.upper(), v=data[k])
    json_data = data.copy()
    for k in ['REMOTE_ADDR', 'HTTP_USER_AGENT', 'HTTP_REFERER']:
        json_data[k] = meta.get(k, None)
    text += "\njson: %s\n" % json.dumps(json_data)
    return text


def takk(request):
    return render(request, 'ui/takk.html', {})
