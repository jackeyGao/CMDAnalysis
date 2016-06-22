from datetime import datetime, timedelta
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from web.models import Box
from web.models import Command
from web.utils import get_domain_from_wsgirequest


def set_cookie(fn):
    def wrapper(*args, **kwargs):
        request = args[0]
        expires = datetime.now() + timedelta(days=7)
        if request.COOKIES.get('user', None):
            _tk = request.COOKIES.get('user', None)
        else:
            _tk = _get_new_csrf_key()

        response = fn(*args, **kwargs)
        response.set_cookie('user', _tk, expires=expires)
        return response
    return wrapper


@set_cookie
def detail(request):
    box = request.GET.get("box", 'none')
    box = get_object_or_404(Box, pk=box)
    return render_to_response('detail.html', locals()) 


@set_cookie
def index(request):
    user = request.COOKIES.get('user', None)
    boxs = Box.objects.filter(user=user)
    for box in boxs:
        box.count = Command.objects.filter(box=box).count()
    domain = get_domain_from_wsgirequest(request)
    return render_to_response('index.html', locals()) 
