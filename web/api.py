# -*- coding: utf-8 -*-
'''
File Name: web/api.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 一  6/20 14:48:35 2016
'''
from __future__ import division
import sys, datetime
import uuid
from datetime import date
from django.shortcuts import get_object_or_404
from django.db.models import Count, F
from rest_framework.decorators import list_route
from rest_framework.parsers import FormParser 
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import filters
from cmdstats import parses
from cmdstats import ParseZshHistoryFile
from cmdstats import ParseBashHistoryFile
from web.models import Command
from web.models import Box

reload(sys)
sys.setdefaultencoding("utf-8")

def handle_uploaded_file(f, box):
    obs = []
    if 'bash' in f.name:
        parse = ParseBashHistoryFile('none')
        shell = "BS"
    elif 'zsh' in f.name:
        parse = ParseZshHistoryFile('none')
        shell = "ZS"

    box.shell = shell
    box.save()

    for line in f.readlines():
        try:
            ob = parse.parse_line(line.strip().encode("utf-8"))

            if ob.has_key('run_time'):
                ts = int(ob["run_time"])
                ob["run_time"] = datetime.datetime.fromtimestamp(ts)

            if ob.has_key('status'):
                ob.pop('status')

            ob["box"] = box
            obs.append(Command(**ob))
        except Exception as e:
            continue

    return obs


class FileUploadView(APIView):
    parser_classes = (FormParser, MultiPartParser, )

    def post(self, request, format='text/plain'):
        box = Box.objects.create(_id=str(uuid.uuid4())[:8])
        obs = handle_uploaded_file(request.data['file'],box)
        Command.objects.bulk_create(obs)
        return Response('http://127.0.0.1:8000/detail/?box=%s' % box.pk)


class CommandList(viewsets.ModelViewSet):
    queryset = Command.objects.all()

    @list_route(methods=['get'], url_path='top')
    def top(self, request, *args, **kwargs):
        filters = {}
        for i in request.GET:
            if i in ('',):
                continue
            value = request.GET.getlist(i)
            if len(value) == 1:
                filters[i] = value[0]
            else:
                filters[i] = value

        queryset = Command.objects.filter(**filters).values('command')
        commands = queryset.annotate(y=Count("command")).order_by("-y")

        for o in commands:
            o["name"] = o["command"]
            o["m"] = round(o["y"] / len(queryset) , 5)

        return Response(commands[:50])
        
    @list_route(methods=['get'], url_path='line')
    def line(self, request, *args, **kwargs):
        filters = {}
        for i in request.GET:
            if i in ('',):
                continue
            value = request.GET.getlist(i)
            if len(value) == 1:
                filters[i] = value[0]
            else:
                filters[i] = value

        qs = Command.objects.filter(**filters).extra({"date": "date(run_time)"})
        qs = qs.values('date').annotate(y=Count("run_time")).order_by('date')

        data = []
        for o in qs:
            if not o["date"]:
                continue
            ts = int((o["date"]- date(1970, 1, 1)).total_seconds() * 1000)
            data.append((ts, o["y"]))


        return Response(data)


