from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('author/<username>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/', views.AuthorListView.as_view(), name='author-list'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms-and-conditions/', views.TermsAndConditionsView.as_view(), name='terms_and_conditions'),
    path('post/<int:pk>', views.PostDetailView.as_view())
]