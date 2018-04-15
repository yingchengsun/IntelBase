'''
Created on Dec 5, 2017

@author: yingc
'''
from pattern.web import Google

for i in range(10):
    for result in Google().search('"Iphone"', start=i+1, count=10):
        print result