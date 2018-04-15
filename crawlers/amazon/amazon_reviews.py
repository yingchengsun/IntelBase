#!/usr/bin/env python
#coding:utf-8
# Written as part of https://www.scrapehero.com/how-to-scrape-amazon-product-reviews-using-python/		
from lxml import html  

import requests
import json,re
from dateutil import parser as dateparser
from time import sleep
import MySQLdb
from collections import OrderedDict

from textblob import TextBlob

def ParseReviews(asin):
	for i in range(8):
		try:
			#This script has only been tested with Amazon.com
			amazon_url  = 'http://www.amazon.com/dp/'+asin
			# Add some recent user agent to prevent amazon from blocking the request 
			# Find some chrome user agent strings  here https://udger.com/resources/ua-list/browser-detail?browser=Chrome
			headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
			page = requests.get(amazon_url,headers = headers)
			page_response = page.text

			parser = html.fromstring(page_response)
			XPATH_AGGREGATE = '//span[@id="acrCustomerReviewText"]'
			XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
			XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'

			XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
			XPATH_PRODUCT_NAME = '//h1//span[@id="productTitle"]//text()'
			XPATH_PRODUCT_PRICE  = '//span[@id="priceblock_ourprice"]/text()'
			
			XPATH_REVIEW_ID = '//div[@data-hook="review"]/@id'
			
			raw_product_price = parser.xpath(XPATH_PRODUCT_PRICE)
			product_price = ''.join(raw_product_price).replace(',','')

			raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
			product_name = ''.join(raw_product_name).strip()
			total_ratings  = parser.xpath(XPATH_AGGREGATE_RATING)
			reviews = parser.xpath(XPATH_REVIEW_SECTION_1)
			
			review_ids=parser.xpath(XPATH_REVIEW_ID)
			
			if not reviews:
				reviews = parser.xpath(XPATH_REVIEW_SECTION_2)
			ratings_dict = {}
			reviews_list = []
			
			if not reviews:
				raise ValueError('unable to find reviews in page')

			#grabing the rating  section in product page

			for ratings in total_ratings:
				extracted_rating = ratings.xpath('./td//a//text()')
				if extracted_rating:
					rating_key = extracted_rating[0] 
					raw_raing_value = extracted_rating[1]
					rating_value = raw_raing_value
					if rating_key:
						ratings_dict.update({rating_key:rating_value})
			#Parsing individual reviews
			i=0
			for review in reviews:				
				XPATH_RATING  = './/i[@data-hook="review-star-rating"]//text()'
				XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
				XPATH_REVIEW_POSTED_DATE = './/a[contains(@href,"/profile/")]/parent::span/following-sibling::span/text()'
				XPATH_REVIEW_TEXT_1 = './/div[@data-hook="review-collapsed"]//text()'
				XPATH_REVIEW_TEXT_2 = './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview'
				XPATH_REVIEW_COMMENTS = './/span[@data-hook="review-comment"]//text()'
				XPATH_AUTHOR  = './/a[contains(@href,"/profile/")]/parent::span//text()'
				XPATH_REVIEW_TEXT_3  = './/div[contains(@id,"dpReviews")]/div/text()'
				
				
				
				raw_review_author = review.xpath(XPATH_AUTHOR)
				raw_review_rating = review.xpath(XPATH_RATING)
				raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
				raw_review_posted_date = review.xpath(XPATH_REVIEW_POSTED_DATE)
				raw_review_text1 = review.xpath(XPATH_REVIEW_TEXT_1)
				raw_review_text2 = review.xpath(XPATH_REVIEW_TEXT_2)
				raw_review_text3 = review.xpath(XPATH_REVIEW_TEXT_3)

				
				author = ' '.join(' '.join(raw_review_author).split()).strip('By')

				#cleaning data
				review_rating = ''.join(raw_review_rating).replace('out of 5 stars','')
				review_header = ' '.join(' '.join(raw_review_header).split())
				review_posted_date = dateparser.parse(''.join(raw_review_posted_date)).strftime('%d %b %Y')
				review_text = ' '.join(' '.join(raw_review_text1).split())

				#grabbing hidden comments if present
				if raw_review_text2:
					json_loaded_review_data = json.loads(raw_review_text2[0])
					json_loaded_review_data_text = json_loaded_review_data['rest']
					cleaned_json_loaded_review_data_text = re.sub('<.*?>','',json_loaded_review_data_text)
					full_review_text = review_text+cleaned_json_loaded_review_data_text
				else:
					full_review_text = review_text
				if not raw_review_text1:
					full_review_text = ' '.join(' '.join(raw_review_text3).split())

				raw_review_comments = review.xpath(XPATH_REVIEW_COMMENTS)
				review_comments = ''.join(raw_review_comments)
				review_comments = re.sub('[A-Za-z]','',review_comments).strip()
				review_dict = {
									'review_id':review_ids[i],
									'review_comment_count':review_comments,
									'review_text':full_review_text,
									'review_posted_date':review_posted_date,
									'review_header':review_header,
									'review_rating':review_rating,
									'review_author':author

								}
				reviews_list.append(review_dict)
				i=i+1
			data = {	
						'asin':asin,
						'ratings':ratings_dict,
						'reviews':reviews_list,
						'url':amazon_url,
						'price':product_price,
						'name':product_name
					}
			return data
		except ValueError:
			print "Retrying to get the correct response"
	
	return {"error":"failed to process the page","asin":asin}
			
def ReadAsin():
	#Add your own ASINs here 
	#AsinList = ['B01ETPUQ6E','B017HW9DEW']

	AsinList = [
        'B00ASURUYQ', 
        'B00YD53JRO', 
        'B01BI2VZEI', 
        'B00YD54GG2',
        'B01N9YOF3R', 
        'B075QJSQLH', 
        'B075QN8NDH',
        'B01MQHADBT',
        'B01MQTJXWZ',
        'B073W5LDKM',
        'B01N8U0046',
        'B074HDDH7B',
        'B015WXL0C6',
        'B072QGG3V7',
    ]
	AsinList = ['B01BI2VZEI']
	'''
	extracted_data = []
	for asin in AsinList:
		print "Downloading and processing page http://www.amazon.com/dp/"+asin
		extracted_data.append(ParseReviews(asin))
		sleep(1)
	f=open('reviews2.json','w')
	#json.dump(extracted_data,f,indent=4)
	json.dump(extracted_data,f)
	f.close()
	'''
	try:
		conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',port=3306,charset='utf8')
		cur=conn.cursor()
		conn.select_db('intelbase')
		'''
		cur.execute("SELECT POLARITY, SUBJECTIVITY FROM amazon_reviews")
		rows = cur.fetchall ()
		for row in rows:
			print type(float(row[0]))
		'''
		cur.execute('create table if not exists amazon_reviews (REVIEW_ID varchar (20) not null primary key, ASIN varchar (20), HEADER varchar(80), TEXT varchar(1000),\
        RATING varchar(20), AUTHOR varchar(20), COMMENT_COUNT varchar(20), DATE varchar(20), POLARITY float(20), SUBJECTIVITY float(20) )\
        DEFAULT CHARSET=utf8mb4')
		
		cur.execute('create table if not exists amazon_ratings (ASIN varchar (20) not null primary key, 1_STAR varchar(20), 2_STAR varchar(20),\
        3_STAR varchar(20), 4_STAR varchar(20), 5_STAR varchar(20))\
        DEFAULT CHARSET=utf8mb4')
				
		
		fileHandle=file('reviews.json')
		fileList = fileHandle.readlines()

		records = json.loads(fileList[0],object_pairs_hook=OrderedDict)
		
		for test_record in records:
			asin = test_record['asin']
			for review in test_record['reviews']:
				print review['review_header']
				#review['review_header'] = review['review_header'].encode('utf-8')
				#review['review_text'] = (review['review_text']).encode('utf-8')
				blob = TextBlob(review['review_text'])
				print blob.sentiment.polarity, blob.sentiment.subjectivity 
				cur.execute('replace into amazon_reviews values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
	                        (review['review_id'], asin, review['review_header'],review['review_text'],review['review_rating'],review['review_author'],review['review_comment_count'],review['review_posted_date'],
							blob.sentiment.polarity, blob.sentiment.subjectivity))
			
			rating = test_record['ratings']
			for i in range(1,6):
				star_number=str(i)+' star'
				if star_number in rating:
					pass
				else:
					rating[star_number] = '0%'

			cur.execute('replace into amazon_ratings values(%s,%s,%s,%s,%s,%s)',
	                        (asin,rating['1 star'],rating['2 star'],rating['3 star'],rating['4 star'],rating['5 star']))
			conn.commit()
		
			
		cur.close()
		conn.close()
		fileHandle.close()
		print len(records),'have been inserted successfully!'

	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
	ReadAsin()