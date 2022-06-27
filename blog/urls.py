from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('subscriber/<email>/<secret_code>', views.SubscriberView.as_view(), name='subscriber'),
    path('author/<username>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/', views.AuthorListView.as_view(), name='author-list'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms-and-conditions/', views.TermsAndConditionsView.as_view(), name='terms_and_conditions'),
    path('category/', views.CategoryListView.as_view(), name="categories"),
    path('category/<title>', views.CategoryDetailView.as_view()),
    path('post/<url>', views.PostDetailView.as_view()),
    path('tags/', views.TagListView.as_view(), name="tags"),
    path('tags/<title>', views.TagDetailView.as_view()),
    path('search/', views.SearchList.as_view())
]
