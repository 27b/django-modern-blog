from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User

from .forms import ContactForm
from .models import Category, Post, Subscriber


class IndexView(View):
    """ TODO """

    def get(self, request):
        return render(request, 'blog/index.html')

    def post(self, request):
        """If the email is valid, check if it already exists
        in the database, if it exists, change the secret
        code and send the email, otherwise create a new
        subscriber and send an email.

        Note:
            This code is written like this for better understanding.
        """
        email = str(request.POST.get('email'))
        if email and '@' in email and 5 < len(email) <= 128:
            subscriber_in_db = Subscriber.objects.filter(email=email).first()
            if subscriber_in_db:
                subscriber_in_db.generate_new_secret_code()
                subscriber_in_db.save()
                subscriber_in_db.send_subscription_email()
            else:
                new_subscriber = Subscriber(email=email)
                new_subscriber.save()
                new_subscriber.send_subscription_email()
        return HttpResponse('We have sent you a link, check your email.')


class IndexView(ListView):
    model = Post
    paginate_by = 6

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['categories'] = Category.get_categories()
    #    return context


class SubscriberView(View):

    def get(self, request, email, secret_code):
        """Check if the email and secret_code is valid."""
        subscriber = Subscriber.objects.filter(email=email).first()
        if subscriber and not subscriber.verified and \
                subscriber.check_secret_code(email, secret_code):
            subscriber.verified = True
            subscriber.save()
            return HttpResponse('Your email has been validated.')
        subscriber.delete_subscriber()
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


class CategoryListView(ListView):
    model = Category
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_name'] = 'Category'
        context['sections'] = [
            {'name': 'Category', 'url': '/category/'}
        ]
        context['posts'] = Post.get_latest_posts()
        return context


class CategoryDetailView(DetailView):
    model = Category
    slug_field = "title"
    slug_url_kwarg = "title"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.object.title
        context['section_name'] = f'Showing posts from {title.capitalize()}'
        context['sections'] = [
            {'name': 'category', 'url': '/category/'},
            {'name': title, 'url': title}
        ]
        context['posts'] = self.object.get_latest_posts()
        return context


class PostDetailView(DetailView):
    model = Post
    slug_field = "url"
    slug_url_kwarg = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.get_similar_posts()
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


class AuthorDetailView(DetailView):
    model = User
    template_name = 'blog/author_detail.html'
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context['object']
        context['posts'] = user.profile.get_latest_posts()[:5]
        return context
