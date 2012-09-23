from django.views.generic import  DetailView
from freevle.virtualcr.models import VirtualClassroom

# Create your views here.
class VirtualCRView(DetailView):
    model = VirtualClassroom
    context_object_name = 'virtualcr'
    slug_url_kwarg='vcr_slug'

    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg, None)

        if slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except self.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


    def get_context_data(self, **kwargs):
        print kwargs
        context = super(DetailView, self).get_context_data(**kwargs)

        context['virtualcr'].sections = context['virtualcr'].section_set.all()

        for section in context['virtualcr'].sections:
            section.attachments = section.attachment_set.all()

            for attachment in section.attachments:
                list_data = attachment.get_plugin().get_list_data()
                attachment.icon = list_data[0]
                attachment.url = list_data[1]
                attachment.label = list_data[2]

            section.attachments = sorted(section.attachments,
                                         key=lambda a: a.order)

        context['object'] = context['virtualcr']

        return context
