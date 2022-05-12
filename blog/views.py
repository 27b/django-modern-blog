from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User

from .forms import ContactForm
from .models import Post, Subscriber


class IndexView(View):

    def get(self, request):
        return render(request, 'blog/index.html')

    def post(self, request):
        email = str(request.POST.get('email'))
        if email and '@' in email and email > 5 and email <= 128:
            subscriber = Subscriber(email=email)
            subscriber.save()
            subscriber.send_subcription_email()
        subscriber.delete_subscriber()
        return HttpResponse('We have sent you a link, check your email.')


class SubscriberView(View):

    def get(self, request, email, secret_code):
        '''Check if the email and secret_code is valid.'''
        subscriber = Subscriber.objects.filter(email=email).first()
        if subscriber and subscriber.verified == False and \
           subscriber.check_random_code(email, secret_code):
            return HttpResponse('Your email has been validated.')
        return HttpResponse('Your email could not be validated, try again later.')


class PrivacyView(View):

    def get(self, request):
        context = {
            'section_name': 'Privacy',
            'sections': [
                {'name': 'Privacy', 'url': '/privacy/'}
            ]
        }
        return render(request, 'blog/privacy.html', context)


class TermsAndConditionsView(View):

    def get(self, request):
        context = {
            'section_name': 'Terms & Conditions',
            'sections': [
                {'name': 'Terms & Conditions', 'url': '/terms-and-conditions/'}
            ]
        }
        return render(request, 'blog/terms_and_conditions.html', context)


class ContactView(View):
    form = ContactForm
    context = {
        'form': None,
        'section_name': 'Contact',
        'sections': [
            {'name': 'Contact', 'url': '/contact/'}
        ]
    }

    def get(self, request):
        self.context['form'] = self.form()
        return render(request, 'blog/contact.html', self.context)

    def post(self, request):
        contact_form = self.form(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            contact_form.instance.send_email()
            contact_form = self.form()
        self.context['form'] = contact_form
        return render(request, 'blog/contact.html', self.context)        
        

class IndexView(ListView):
    model = Post
    paginate_by = 6


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.get_similar_posts()
        return context


class AuthorDetailView(DetailView):
    model = User
    template_name = 'blog/author_detail.html'
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context['object']
        context['posts'] = user.profile.get_last_posts()[:5]
        return context


class AuthorListView(ListView):
    model = User
    template_name = 'blog/author_list.html'
    paginate_by = 6

    def get_queryset(self):
        return User.objects.order_by('date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Authors'
        context['sections'] = [{'name': 'Authors', 'url': '/authors/'}]
        return context
