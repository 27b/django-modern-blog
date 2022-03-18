from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Post


class IndexView(View):
    methods = ['GET']

    def get(self, request):
        return render(request, 'blog/index.html')


class IndexView(ListView):
    model = Post
    paginate_by = 6


class PostDetailView(DetailView):
    model = Post
