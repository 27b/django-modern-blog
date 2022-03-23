from django import forms
from .models import Contact


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
                'placeholder': 'jhondoe@email.com'
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
