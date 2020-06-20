from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from .models import Statement, Page
from .forms import AnwserProposeForm


class HomePageView(TemplateView):
    template_name = 'HomePage.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statement'] = Statement.objects.filter(entry=True).order_by("?").first()
        context['form'] = AnwserProposeForm()
        return context

class StatementView(DetailView,FormView):
    form_class = AnwserProposeForm
    model = Statement
    success_url = '?anwser_added_waiting_for_accept=1'
    def form_valid(self, form):
        self.object = self.get_object()
        if form.cleaned_data['make_new_statement']:
            zdanie = Statement.objects.create(text = form.cleaned_data['new_statement'])
        else:
            zdanie = Statement.objects.get(id = form.cleaned_data['goto_statement'])
        self.object.add_option(form.cleaned_data['text'],zdanie,accepted=False)
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        return context

class PageView(DetailView):
    model = Page

class SearchStatementView(TemplateView):
    template_name = 'SearchStatment.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            q = self.request.GET['q']
            if len(q)>1: context['found'] = Statement.objects.filter(text__contains=q)
            else: context['found'] = []
        except Exception as e:
            context['found'] = []
        return context
