from django.shortcuts import redirect

"""Middleware that restricts superusers to only access the admin panel.
If a superuser tries to access any non-admin URL, they are redirected to /admin/."""
class BlockSuperuserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated and is a superuser
        if request.user.is_authenticated and request.user.is_superuser:
            # If the requested path does NOT start with /admin/, redirect to admin panel
            if not request.path.startswith('/admin/'):
                return redirect('/admin/')
        # Otherwise, proceed with the normal request/response cycle
        return self.get_response(request)