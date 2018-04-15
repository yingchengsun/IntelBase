#coding:utf-8
'''
Created on Dec 13, 2017

@author: yingc
'''
import MySQLdb
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from os import path

ratings=[0,0,0,0,0]
polarity_count=[0,0,0,0]
subjectivity_count=[0,0,0,0]

d = path.dirname(__file__)

def initialize_db(query):

    try:
        conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',port=3306,charset='utf8')
        cur=conn.cursor()
        conn.select_db('intelbase')
        
        cur.execute("SELECT ASIN FROM query where QUERY=%s", query)
        asin = cur.fetchall()[0][0]
        
        
        cur.execute("SELECT POLARITY FROM amazon_reviews where ASIN=%s", asin)
        polarity_db = cur.fetchall ()
        polarity_list = [x[0] for x in polarity_db]
        global polarity_count
        polarity_count=[0,0,0,0]
        for x in polarity_list:
            if x>=-1 and x<-0.5:
                polarity_count[0]=polarity_count[0]+1
            if x>=-0.5 and x<0:
                polarity_count[1]=polarity_count[1]+1
            if x>=0 and x<0.5:
                polarity_count[2]=polarity_count[2]+1
            if x>=0.5 and x<=1:
                polarity_count[3]=polarity_count[3]+1
        
        
        cur.execute("SELECT SUBJECTIVITY FROM amazon_reviews where ASIN=%s", asin)
        subjectivity_db = cur.fetchall ()
        subjectivity_list = [x[0] for x in subjectivity_db]
        global subjectivity_count
        subjectivity_count=[0,0,0,0]
        for x in subjectivity_list:
            if x>=0 and x<0.25:
                subjectivity_count[0]=subjectivity_count[0]+1
            if x>=0.25 and x<0.5:
                subjectivity_count[1]=subjectivity_count[1]+1
            if x>=0.5 and x<0.75:
                subjectivity_count[2]=subjectivity_count[2]+1
            if x>=0.75 and x<=1:
                subjectivity_count[3]=subjectivity_count[3]+1
        
        
        cur.execute("SELECT ASIN, NAME,CATEGORY,IMAGE, AVAILABILITY FROM amazon_product where ASIN=%s", asin)

        product_info = cur.fetchall()[0]

        '''
        print product_info[0]
        print product_info[1]
        print product_info[2]
        print product_info[3]
        '''
        cur.execute("SELECT 1_STAR,2_STAR,3_STAR,4_STAR,5_STAR FROM amazon_ratings where ASIN=%s", asin)
        ratings_db = cur.fetchall()
        ratings_list=list(ratings_db[0])
        global ratings
        ratings = [int(x.strip('%')) for x in ratings_list]
                
        cur.execute("SELECT TEXT FROM amazon_reviews where ASIN=%s", asin)
        reviews_db = cur.fetchall()
        reviews_list = [x[0] for x in reviews_db]
        reviews_str = " ".join(reviews_list)
        
        cur.close()
        conn.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return list(product_info),reviews_str
    
    
def rating_chart(query):
      # The slices will be ordered and plotted counter-clockwise.
    plt.title('Rating',fontweight='bold') 
    
    labels = '1_STAR','2_STAR','3_STAR','4_STAR','5_STAR'
    colors = ['lightskyblue','darkgray', 'gold','yellowgreen', 'lightcoral']
    explode = (0, 0, 0, 0,0.05)  # only "explode" the 5th slice (i.e. '5_STAR')
    plt.pie(ratings,  labels=labels, colors=colors,explode=explode,
            autopct='%1.0f%%', shadow=False, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.tight_layout(pad=0)
    plt.savefig('E:/workspace/IntelBase/static/images/amazon_rating_chart_'+query+'.png')
    plt.close("all")
    #plt.show()
    print 'amazon_rating_chart'
    
def polarity_chart(query):
    
    plt.title('Polarity',fontweight='bold') 
    plt.xlabel("range", color='blue', fontweight='bold') 
    plt.ylabel("count", color='red', fontweight='bold') 
    xticks=[-0.75, -0.25, 0.25, 0.75]
    bar_width=0.48
    colors = ['royalblue', 'royalblue','royalblue', 'royalblue']
    plt.bar(xticks, polarity_count, width = bar_width, edgecolor='none',color=colors)
    plt.savefig('E:/workspace/IntelBase/static/images/amazon_polarity_chart_'+query+'.png')
    plt.close("all")
    print 'amazon_polarity_chart'
    
def subjectivity_chart(query):
   
    plt.title('Subjectivity',fontweight='bold') 
    plt.xlabel("range", color='blue', fontweight='bold') 
    plt.ylabel("count", color='red', fontweight='bold') 
    xticks=[-0.75, -0.25, 0.25, 0.75]
    bar_width=0.48
    colors = ['tomato', 'tomato','tomato', 'tomato']
    plt.bar(xticks, subjectivity_count, width = bar_width, edgecolor='none',color=colors)
    plt.savefig('E:/workspace/IntelBase/static/images/amazon_subjectivity_chart_'+query+'.png')
    plt.close("all")
    print 'amazon_subjectivity_chart'

def wordcloud_chart(text,query):
   
    # Generate a word cloud image
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
    
    plt.savefig('E:/workspace/IntelBase/static/images/amazon_reviews_wordcloud_'+query+'.png', facecolor='k', bbox_inches='tight')
    plt.close("all")
    print 'amazon_reviews_wordcloud'
    
if __name__ == '__main__':
    #asin='B075QJSQLH'
    query = 'Iphone 8'
    results=initialize_db(query)
    product_info=results[0]
    wordcloud_chart(results[1], query)
    rating_chart(query)
    subjectivity_chart(query)
    polarity_chart(query)
    