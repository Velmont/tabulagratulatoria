from django.shortcuts import render

from core.forms import EntryForm


def home(request):
    return render(request, 'ui/home.html', {})


def adder(request):
    form = EntryForm()
    return render(request, 'ui/adder.html',
                  {
                      'form': form,
                  })
