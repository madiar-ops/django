from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from bboard.models import Bb, Rubric
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, FormView, CreateView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from bboard.forms import BbForm
from bboard.models import IceCreamKiosk

import requests
def index(request):
    # template = loader.get_template('index.html')
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()

    context = {'bbs': bbs, 'rubrics': rubrics}
    # return HttpResponse(template.render(context, request))
    return render(request, 'index.html', context)

def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'by_rubric.html', context)

class BbCreateView(CreateView):
    template_name = 'create.html'
    form_class = BbForm
    # success_url = '/'
    success_url = reverse_lazy('index')


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['rubrics'] = Rubric.objects.all()
    return context



def home(request):
    return render(request, 'home.html')


def sorted_list(request):
    return render(request, 'list.html')


def card_view(request):
    return render(request, 'card.html')

def login_view(request):
    return render(request, 'login.html')


def fake_api_view(request):
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = []
    if response.status_code == 200:
        posts = response.json()[:5]
    context = {'posts': posts}
    return render(request, 'fake_api.html', context)

class BbListView(ListView):
    model = Bb
    template_name = 'index.html'
    context_object_name = 'bbs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbRubricBbsView(ListView):
    model = Bb
    template_name = 'by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = get_object_or_404(Rubric, pk=self.kwargs['rubric_id'])
        return context


class BbCreateView(FormView):
    template_name = 'create.html'
    form_class = BbForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        bb = form.save()
        return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': bb.rubric.pk}))


class BbDetailView(DetailView):
    model = Bb
    template_name = 'bb_detail.html'
    context_object_name = 'bb'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbEditView(UpdateView):
    model = Bb
    template_name = 'bb_form.html'
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbDeleteView(DeleteView):
    model = Bb
    template_name = 'bb_confirm_delete.html'
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

def kiosks_list(request):
    kiosks = IceCreamKiosk.objects.prefetch_related("ice_creams").all()
    return render(request, "kiosks_list.html", {"kiosks": kiosks})
