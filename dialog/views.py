from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.urls import reverse

from graphviz import Digraph, Graph

from .models import Statement, Page, Anwser
from .forms import AnwserProposeForm


class GraphView(TemplateView):
    template_name = 'Graph.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dot = Digraph(comment='Graf rozmowy', format='svg')
        # dot = Graph('Graf rozmowy', format='svg')
        for s in Statement.objects.all():
            dot.node("s_"+str(s.id), str(s),style="filled",shape="note",fillcolor="#8ad9cf",URL=reverse('Statement',args=(s.id,)))
        for a in Anwser.objects.all():
            dot.node("a_"+str(a.id), str(a),style="filled",shape="signature",fillcolor="#e4b78a")

            dot.edge("a_"+str(a.id), "s_"+str(a.goto.id),label="Przejdź do")
            for s in a.statement_set.all():
                dot.edge("s_"+str(s.id),"a_"+str(a.id))
        context['graph'] = dot.pipe().decode('utf-8')
        return context

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
