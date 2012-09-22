from django.shortcuts import render_to_response
from django.template import RequestContext

def changepassword(request):
    data = RequestContext(request)
    if request.method == 'POST':
        user = request.user
        oldpass = request.POST['old-password']
        newpass = request.POST['new-password']
        confirmpass = request.POST['confirm-password']

        if newpass != confirmpass:
            data['success'] = False
        elif user.has_usable_password() and user.check_password(oldpass):
            user.set_password(request.POST['new-password'])
            user.save()
            data['success'] = True
    return render_to_response('user/settings.html', data)
