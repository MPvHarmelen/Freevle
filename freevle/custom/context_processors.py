def cms(request):
    from freevle.cms.models import Page
    return {'pages':Page.objects.all()}

def  app_list(request):
    if request.path.split('/')[0] == 'admin':
        pass
