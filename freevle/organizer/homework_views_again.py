# Just a quiet place to work
# The below is already there in organizer.views I'll delete it when moving back.
import datetime
import warnings
import copy

from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from freevle.organizer.models import *
from freevle.organizer.views import *
# The above is already there in organier.views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

@login_required
def get_course_view(request):
    if request.user.groups.filter(name='teachers'):
        if request.method == 'POST':
            url = 'organizer-update-homework'
            kwargs = {'course':request.POST['course']}
            return HttpResponseRedirect(reverse(url, kwargs=kwargs))
        else:
            courses = sorted(request.user.gives_courses.all(), key=lambda a: a.name)
            return render_to_response('organizer/course_form.html',
                                      {'courses':courses})
    else:
        raise PermissionDenied
