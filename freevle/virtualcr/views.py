from django.views.generic import  DetailView
from freevle.virtualcr.models import VirtualClassroom

# Create your views here.
class VirtualCRView(DetailView):
    model = VirtualClassroom
    context_object_name = 'virtualcr'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        context['virtualcr'].sections = context['virtualcr'].section_set.all()

        for section in context['virtualcr'].sections:
            section.attachments = section.attachment_set.all()

            for attachment in section.attachments:
                list_data = attachment.plugin.get_list_data()
                attachment.url = list_data[0]
                attachment.label = list_data[1]

        context['object'] = context['virtualcr']

        return context
