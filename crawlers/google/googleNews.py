'''
Created on Dec 5, 2017

@author: yingc
'''

from pattern.web    import Newsfeed, plaintext
from pattern.db     import date
from pattern.vector import Model, Document, LEMMA
  
news, url = {}, 'http://news.google.com/news?output=rss'
for story in Newsfeed().search(url, cached=False):
    d = str(date(story.date, format='%Y-%m-%d'))
    s = plaintext(story.description)

    # Each key in the news dictionary is a date: news is grouped per day.
    # Each value is a dictionary of id => story items.
    # We use hash(story.description) as a unique id to avoid duplicate content.
    news.setdefault(d, {})[hash(s)] = s
   

m = Model()
for date, stories in news.items():
    s = stories.values()
    s = ' '.join(s).lower()
    # Each day of news is a single document.
    # By adding all documents to a model we can calculate tf-idf.
    print s
    m.append(Document(s, stemmer=LEMMA, exclude=['news', 'day'], name=date))



for document in m:
    print document
    '''
    print document.name
    print document.keywords(top=10)
    '''

