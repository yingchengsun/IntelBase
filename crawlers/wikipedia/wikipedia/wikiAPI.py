#coding:utf-8
'''
Created on Dec 4, 2017

@author: yingc
'''
import wikipedia
#print wikipedia.summary("Wikipedia")
# Wikipedia (/ˌwɪkɨˈpiːdiə/ or /ˌwɪkiˈpiːdiə/ WIK-i-PEE-dee-ə) is a collaboratively edited, multilingual, free Internet encyclopedia supported by the non-profit Wikimedia Foundation...

#print wikipedia.search("Barack")
# [u'Barak (given name)', u'Barack Obama', u'Barack (brandy)', u'Presidency of Barack Obama', u'Family of Barack Obama', u'First inauguration of Barack Obama', u'Barack Obama presidential campaign, 2008', u'Barack Obama, Sr.', u'Barack Obama citizenship conspiracy theories', u'Presidential transition of Barack Obama']

ny = wikipedia.page("Tim Cook")
print ny.title
# u'New York'
print ny.url
# u'http://en.wikipedia.org/wiki/New_York'
#print ny.content
# u'New York is a state in the Northeastern region of the United States. New York is the 27th-most exten'...
print ny.links
#print ny.coordinates
print ny.categories
print ny.images
print ny.references
print ny.sections
# u'1790 United States Census'

wikipedia.set_lang("fr")
print wikipedia.summary("Facebook", sentences=1)