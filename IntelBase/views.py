from django.http import HttpResponse
#from db.models import Student
from django.shortcuts import render

def hello(request):
    return HttpResponse("Hello world! This is my first trial.[fuck]")
'''
def add(request):
    s = Student(id=101, name='handsomeguy')
    s.save()
    return HttpResponse("record added!")
'''
def home(request):
    nameList=["HTML", "CSS", "jQuery", "Python", "Django"]
    return render(request, 'hh.html', {'nameList': nameList})