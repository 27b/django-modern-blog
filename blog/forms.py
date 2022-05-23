from django import forms
from .models import Contact, Subscriber


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'subject': 'Subject',
            'message': 'Your Message'
        }
        widgets = {
            'name': forms.TextInput(attrs = {
                'class': 'form-control rounded',
                'placeholder': 'John Doe'
            }),
            'email': forms.TextInput(attrs = {
                'class': 'form-control rounded',
                'placeholder': 'johndoe@email.com'
            }),
            'subject': forms.TextInput(attrs = {
                'class': 'form-control rounded',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs = {
                'class': 'form-control rounded',
                'placeholder': 'Your Message'
            }),
        }


class SubscriberForm(forms.ModelForm    ):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter yout email'
                }
            ),
        }