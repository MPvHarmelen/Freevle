from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator

from freevle.users.models import UserProfile

class ProfileObjectMixin(SingleObjectMixin):
    """
    Provides views with the current user's profile.
    """
    model = UserProfile

    def get_object(self):
        """Return's the current users profile."""
        try:
            return self.request.user.get_profile()
        except UserProfile.DoesNotExist:
            raise NotImplemented(
                "What if the user doesn't have an associated profile?")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Ensures that only authenticated users can access the view."""
        klass = ProfileObjectMixin
        return super(klass, self).dispatch(request, *args, **kwargs)

class ProfileUpdateView(ProfileObjectMixin, UpdateView):
    """
    A view that displays a form for editing a user's profile.

    Uses a form dynamically created for the `Profile` model and
    the default model's update template.
    """
    pass  # That's All Folks!

def changepassword(request):
    data = RequestContext(request)
    if request.method == 'POST':
        user = request.user
        oldpass = request.POST['old-password']
        newpass = request.POST['new-password']
        confirmpass = request.POST['confirm-password']

        if newpass != confirmpass:
            data['success'] = False
        elif user.has_usable_password() and user.check_password(oldpass):
            user.set_password(request.POST['new-password'])
            user.save()
            data['success'] = True
    return render_to_response('user/settings.html', data)
