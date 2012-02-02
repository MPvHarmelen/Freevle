def cms(request):
	from cygy.cms.models import Page
	return {'Pages':Page.objects.all()}