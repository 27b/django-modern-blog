from uuid import uuid4

from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.mail import send_mail
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=512)
    image = models.ImageField(upload_to='images/profile/')

    def __str__(self) -> str:
        return self.user.username
    
    def get_last_posts(self):
        return Post.objects.filter(
            author=self.user.id
        ).order_by(
            '-datetime'
        )


class Category(models.Model):
    title = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=512)
    content = models.TextField()
    tags = ArrayField(models.CharField(max_length=32, blank=True))
    image = models.ImageField(upload_to='images/')
    last_modified = models.DateField(auto_now=True)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-datetime']

    def __str__(self) -> str:
        return self.title
    
    def get_similar_posts(self) -> list or False:
        posts = Post.objects.filter(
            category=self.category
        ).order_by(
            '-datetime'
        )[:2]
        if len(posts) > 0:
            return posts
        return False


class Contact(models.Model):
    name = models.CharField(null=False, max_length=128)
    email = models.EmailField(null=False, max_length=256)
    subject = models.CharField(null=False, max_length=256)
    message = models.TextField(null=False, max_length=1024)

    def __str__(self) -> str:
        return f'{self.name} <{self.email}> {self.subject}'

    def send_email(self) -> None:
        send_mail(
            self.subject,
            f'{self.name}: {self.message}',
            self.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )


class Subscriber(models.Model):
    email = models.CharField(unique=True, null=False, max_length=128)
    random_code = models.CharField(max_length=32, default=uuid4().hex)
    verified = models.BooleanField(default=False)

    def __check_if_subscriber_in_db(self, email: str) -> bool:
        '''Check if the email exists in the database. 
        
        Args:
            email: str
        '''
        if Subscriber.objects.filter(email=email).first():
            return True
        return False

    def generate_new_secret_code(self) -> None:
        self.secret_code = uuid4().hex

    def delete_subscriber(self) -> None:
        '''Use this method if the user wants to unsubscribe or
        if there were one or more failed attempts to access
        /subscriber/ with wrong credentials.'''
        # Equivalent: Subscriber.objects.filter(email=self.email).delete()
        self.delete()

    def send_subscription_email(self) -> None:
        '''Send an email using the attributes of the object.'''
        if self.__check_if_subscriber_in_db(self.email):
            subscriber = Subscriber.objects.filter(email=email).first()
            email = subscriber.email
            random_code = subscriber.random_code
            link = f'https://orion-b.com/subscribe/{email}/{random_code}'
            send_mail(
                'Orion B: Subscribe for our monthly newsletter.',
                f'If you want to subscribe, access this link:\br {link}',
                'noreplay@orion-b.com',
                [email],
                fail_silently=False,
            )

    def check_secret_code(self, email: str, random_code: str) -> bool:
        '''Check if the email and the secret code match those
        found in the database.'''
        if self.email == email and self.random_code == random_code:
            return True
        return False


admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Contact)
admin.site.register(Subscriber)
