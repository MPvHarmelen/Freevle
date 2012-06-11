from django.core import urlresolvers
from django.template import RequestContext
from freevle import personalsettings

def cms(request):
    from freevle.cms.models import Page
    return {'pages':Page.objects.all()}

def  app_list(request):
    applist = []
    if request.path.split('/')[1] == 'admin':
        user = request.user
        for i in personalsettings.ADMIN_STRUCT:
            if not user.has_module_perms(i):
                continue
            changelist = '_'.join(i[1].split('.')) + '_changelist'
            applist.append((i[0], urlresolvers.reverse('admin:' + changelist)))

    return {'apps': applist}


# Made this, found out it's probably not actually necessary. Fuck.
#
# import imp
#            module = ['freevle',] + i[1].split('.')
#            path = '/'.join(module[1:])
#            if len(module) > 2:
#                module.insert(2, 'models')
#                path = '/'.join(module[1:-1]) + '.py'
#            module = '.'.join(module)
#
#            mod = imp.load_source(module, path)
