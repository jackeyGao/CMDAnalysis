# -*- coding: utf-8 -*-
'''
File Name: web/forms.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 一  6/20 14:41:39 2016
'''

from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
