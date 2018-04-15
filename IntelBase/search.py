'''
Created on Oct 25, 2017

@author: yingcheng
'''
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.views.decorators import csrf
import amazon_visualization as av

def search_form(request):
    return render_to_response('search_form.html')

def search_post(request):
    ctx ={}
    if request.POST:
        ctx['rlt'] = request.POST['q']
    return render(request, "search_form.html", ctx)

def search(request):
    request.encoding = 'utf-8'
    print request.GET
    query = request.GET['query']
    if query=='':
        message = 'your query is empty.'
        return HttpResponse(message)
    else:
        #message = 'your query is:' + request.GET['q']
        results=av.initialize_db(query)
        
        amazon_product_introduction=results[0]
        '''
        av.wordcloud_chart(results[1])
        av.polarity_chart()
        av.subjectivity_chart()
        av.rating_chart()
        '''
        return render(request, 'Index/admin/layout1/dashboard.html',{'query': query,'amazon_product_introduction':amazon_product_introduction})
    

    
    
