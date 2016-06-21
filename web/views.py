
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from web.models import Box


def detail(request):
    box = request.GET["box"]
    box = get_object_or_404(Box, pk=box)
    return render_to_response('detail.html', locals()) 

def index(request):
    return render_to_response('index.html', locals()) 
