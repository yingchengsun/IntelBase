'''
Created on Apr 17, 2018

@author: yingc
'''
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def wordcloud_chart(text,query):
    wordcloud = WordCloud(width=1600, height=800).generate(text)
    
    # Display the generated image:
    # the matplotlib way:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    
    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure( figsize=(20,10), facecolor='k')
    
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    
    plt.savefig('E:/wordcloud_'+query+'.png', facecolor='k', bbox_inches='tight')
    plt.close("all")
    print 'amazon_reviews_wordcloud'

if __name__ == '__main__':
    with open('subreddits_title-publicDescription.txt','r') as ss:
        w = ss.read()
        wordcloud_chart(w, 'query')