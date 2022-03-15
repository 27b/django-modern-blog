from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView


class IndexView(View):
    methods = ['GET']

    def get(self, request):
        return render(request, 'blog/index.html')
