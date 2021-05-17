from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView

from utilsapp.models import File
from utilsapp.forms import FilesForm
from utilsapp.services import CheckCsv, handle_uploaded_file
from utilsapp import tasks


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
            handle_uploaded_file(form.files['psp_file'], request.FILES['psp_file'].name)
            handle_uploaded_file(form.files['db_file'], request.FILES['db_file'].name)

            tasks.check_csv.delay(request.FILES['psp_file'].name, request.FILES['db_file'].name, is_deposit=form.cleaned_data['is_deposit'])

        return HttpResponseRedirect(reverse('utilsapp:index'))