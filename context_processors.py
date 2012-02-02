def cms(request):
	from cygy.cms.models import Page
	return {'pages':Page.objects.all()}