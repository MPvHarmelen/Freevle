from django.template.response import TemplateResponse
from django.views.generic.detail import DetailView
from django.views.generic.base import View

# Create your views here.
class UserView(View):

    '''
    day1 = queryset
    day2 = queryset
    day3 = queryset
    > announcements = queryset
    > comming_homework = queryset
    > is_weekend = None or 0 or 1
    > days = [day1, day2, day3]
    
    To write:
    get_comming_homework()
    get_anouncements()
    get_is_weekend()
    get_days()
    
    '''
    user_url_kwarg = 'user'
    
    def get_days(self):   ## << Here
        """
        Get the list of items for this view. This must be an interable, and may
        be a days (in which qs-specific behavior will be enabled).
        """
        if self.days is not None:
            days = self.days
        else:
            user = self.kwargs.get(self.user_url_kwarg, None)
            if user is not None:
                
        return days

    def get_queryset(self):   ## << Here
        """
        Get the list of items for this view. This must be an interable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(u"'%s' must define 'queryset' or 'model'"
                                       % self.__class__.__name__)
        return queryset

    # -- Done --
    ## Original    
    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [self.template_name]
    
    ## Original
    response_class = TemplateResponse
    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        return self.response_class(
            request = self.request,
            template = self.get_template_names(),
            context = context,
            **response_kwargs
        )

    ## Edited
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    ## Edited
    def get_context_data(self):
        """
        Get the context for this view.
        """
        self.announcements = self.get_announcements()
        self.comming_homework = self.get_comming_homework()
        self.is_weekend = self.get_is_weekend()
        self.days = self.get_days()

        context = {
            'announcements': announcements,
            'comming_homework': comming_homework,
            'is_weekend': is_weekend,
            'days': days,
        }

        return context


# I'm just leaving this here for now if I want to use parts later
class UserDetailView(DetailView):
    username_field = 'username'
    username_url_kwarg = 'username'

    def get_object(self, queryset=None):
        

        # Use a custom queryset if provided
        if queryset is None:
            queryset = self.## Needs queryset()

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
