from django.views.generic.detail import DetailView

# Create your views here.
class UserView(DetailView):
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
