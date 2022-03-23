from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import ContactForm
from .models import Post


class IndexView(View):

    def get(self, request):
        return render(request, 'blog/index.html')


class PrivacyView(View):

    def get(self, request):
        return render(request, 'blog/privacy.html')


class TermsAndConditionsView(View):

    def get(self, request):
        return render(request, 'blog/terms_and_conditions.html')


class ContactView(View):
    form = ContactForm

    def get(self, request):
        context = {'form': self.form()}
        return render(request, 'blog/contact.html', context)

    def post(self, request):
        contact_form = self.form(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            contact_form.instance.send_email()
            contact_form = self.form()
        return render(request, 'blog/contact.html', {'form': contact_form})
        
        

class IndexView(ListView):
    model = Post
    paginate_by = 6


class PostDetailView(DetailView):
    model = Post
