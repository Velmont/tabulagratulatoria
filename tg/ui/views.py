from django.shortcuts import render
from django.http import HttpResponseRedirect

from core.forms import EntryForm


def home(request):
    return render(request, 'ui/home.html', {})


def adder(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/takk')
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


def takk(request):
    return render(request, 'ui/takk.html', {})
