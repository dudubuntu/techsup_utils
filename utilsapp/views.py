from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from utilsapp.models import File
from utilsapp.forms import FilesForm
from utilsapp.services import CheckCsv


class IndexView(ListView):
    model = File
    template_name = 'utilsapp/index.html'
    queryset_name = 'file_list'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FilesForm
        return context

    def post(self, request):
        form = FilesForm(request.POST, request.FILES)
        if form.is_valid():
            pass
            # fh = CheckCsv().check_neteller()
        return HttpResponseRedirect(reverse('utilsapp:index'))