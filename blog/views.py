from django.shortcuts import render
from django.views import View


class Index(View):
    methods = ['GET']

    def get(self, request):
        return render(request, 'blog/index.html')

