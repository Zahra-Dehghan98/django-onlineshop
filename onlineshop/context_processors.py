from .models import Category

""" Context processor to make all categories available globally in templates.Returns a dictionary containing all Category objects"""
def categories(request):
    return {
        'categories' : Category.objects.all()
        }