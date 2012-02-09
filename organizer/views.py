from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin, View

# Create your views here.
class UserView(TemplateResponseMixin, View):

    def get_lessonset(self):
        """
        Get the list of items for this view. This must be an interable, and may
        be a lessonset (in which qs-specific behavior will be enabled).
        """
        if self.lessonset is not None:
            lessonset = self.lessonset
            if hasattr(lessonset, '_clone'):
                lessonset = lessonset._clone()
        elif self.model is not None:
            lessonset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(u"'%s' must define 'lessonset' or 'model'"
                                       % self.__class__.__name__)
        return lessonset


# I'm just leaving this here for now if I want to use parts later
class UserDetailView(DetailView):
    username_field = 'username'
    username_url_kwarg = 'username'

    def get_object(self, queryset=None):
        

        # Use a custom queryset if provided
        if queryset is None:
            queryset = self.get_queryset()

        username = self.kwargs.get(self.username_url_kwarg, None)

        # Try looking up by username.
        if username is not None:
            username_field = self.username_field
            queryset = queryset.filter(**{username_field: username})

        # If none of those are defined, it's an error.
        else:
            raise AttributeError(u'Generic detail view {} must be called with '
                                 u'a username.'.format(self.__class__.__name__))

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(
                _(u'No {verbose_name} found matching the query').format(
                    verbose_name=queryset.model._meta.verbose_name
                    )
                )
        return obj
