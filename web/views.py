from datetime import datetime, timedelta
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import _get_new_csrf_key
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


def detail(request):
    box = request.GET.get("box", 'none')
    box = get_object_or_404(Box, pk=box)
    return render_to_response('detail.html', locals()) 


def index(request):
    user = request.COOKIES.get('user', None)
    if not user:
        user = _get_new_csrf_key()

    boxs = Box.objects.filter(user=user)
    domain = get_domain_from_wsgirequest(request)
    for box in boxs:
        box.count = Command.objects.filter(box=box).count()

    # set cookie 
    expires = datetime.now() + timedelta(days=7)
    response = render_to_response('index.html', locals()) 
    response.set_cookie('user', _tk, expires=expires)
    return response

