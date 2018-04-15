# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#from db.models import Student
from django.shortcuts import HttpResponseRedirect,Http404,HttpResponse,render_to_response

# Create your view here.
def home(request):
    '''
    context = {}
    return render(request, 'Index/home.html', context)
    '''
    '''
    msglist = Student.objects.all()
    msglist.order_by('id')
    context = {'msglist': msglist}
    '''
    #return render(request, 'Index/show.html', context)
    #return render(request, 'Index/admin/layout1/dashboard.html', context)
    return render(request, 'Index/admin/layout1/dashboard.html',{'query': 'Iphone 6'})


