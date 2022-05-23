from .models import Category
from .forms import SubscriberForm

def list_of_categories(request) -> dict:
    """Adding categories to context in all views."""
    return {
        'categories': Category.get_categories(),
        'subscriber_form': SubscriberForm
    }
