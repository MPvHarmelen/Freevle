def cms(request):
	from freevle.cms.models import Page
	return {'pages':Page.objects.all()}