from .models import Category


def list_of_categories(request) -> dict:
    """Adding categories to context in all views."""
    return {
        'categories': Category.get_categories()
    }
