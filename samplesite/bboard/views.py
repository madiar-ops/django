from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from bboard.models import Bb, Rubric
from django.urls import reverse_lazy
from django.views.generic import CreateView
from bboard.forms import BbForm
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


