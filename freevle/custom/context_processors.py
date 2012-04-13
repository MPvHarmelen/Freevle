def cms(request):
	from schoolr.cms.models import Page
	return {'pages':Page.objects.all()}