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


        # To Do
    template_name_suffix = '_list'

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if get_template is overridden.
        """
        try:
            names = super(MultipleObjectTemplateResponseMixin, self).get_template_names()
        except ImproperlyConfigured:
            # If template_name isn't specified, it's not a problem --
            # we just start with an empty list.
            names = []

        # If the list is a queryset, we'll invent a template name based on the
        # app and model name. This name gets put at the end of the template
        # name list so that user-supplied names override the automatically-
        # generated ones.
        if hasattr(self.object_list, 'model'):
            opts = self.object_list.model._meta
            names.append("%s/%s%s.html" % (opts.app_label, opts.object_name.lower(), self.template_name_suffix))

            return names





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
