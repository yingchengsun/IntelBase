#coding: utf-8
from lxml import html  
import unicodecsv as csv
import requests
from exceptions import ValueError
from time import sleep
import re,urllib
import argparse

def parse(url):
	print url
	response = requests.get(url).text
	parser = html.fromstring(response)
	reviews_list = parser.xpath("//div[@class='review review--with-sidebar']")
	scraped_data = []
	for review in reviews_list:
		raw_review_date = review.xpath(".//span[@class='rating-qualifier']//text()")
		raw_review_rating = review.xpath(".//div[contains(@class,'rating-large')]/@title")
		raw_review_text = review.xpath(".//div[@class='review-content']//p/text()")
		raw_review_useful_count = review.xpath('.//span[contains(text(),"Useful")]/following-sibling::span//text()')
		raw_review_funny_count = review.xpath('.//span[contains(text(),"Funny")]/following-sibling::span[@class="count"]/text()')
		raw_review_cool_count = review.xpath('.//span[contains(text(),"Cool")]/following-sibling::span//text()')
		raw_review_author = review.xpath('.//li[@class="user-name"]//a//text()')
		raw_review_author_link = review.xpath('.//li[@class="user-name"]//a/@href')[0]
		review_author_location = review.xpath('.//li[contains(@class,"user-location")]//b/text()')
		raw_friend_count = review.xpath('.//li[contains(@class,"friend-count")]//b/text()')
		raw_author_review_count = review.xpath('.//li[contains(@class,"review-count")]//b/text()')
		raw_author_photo_count = review.xpath('.//li[contains(@class,"photo-count")]//b/text()')

		review_date = ''.join(raw_review_date).strip() if raw_review_date else None
		review_rating = ''.join(raw_review_rating).strip() if raw_review_rating else None
		review_content = ''.join(raw_review_text).strip() if raw_review_text else None
		useful_count = ''.join(raw_review_useful_count).strip() if raw_review_useful_count else 0
		funny_count = ''.join(raw_review_funny_count).strip() if raw_review_funny_count else 0
		cool_count =  ''.join(raw_review_cool_count).strip() if raw_review_cool_count else 0
		author = ''.join(raw_review_author).strip() if raw_review_author else None
		author_location = ''.join(review_author_location).strip() if review_author_location else None
		friend_count = ''.join(raw_friend_count).strip() if raw_friend_count else 0
		author_reviews_count = ''.join(raw_author_review_count).strip() if raw_author_review_count else 0
		photo_count = ''.join(raw_author_photo_count).strip() if raw_author_photo_count else 0
		raw_review_author_link='https://www.yelp.com'+raw_review_author_link

		if review_rating:
			ratings = re.findall("\d+[.,]?\d+",review_rating)[0]
		else:
			ratings = 0
		
		data = {	
					'review_date':review_date,
					'review_rating':ratings,
					'review_content':review_content,
					'useful_count':useful_count,
					'funny_count':funny_count,
					'cool_count':cool_count,
					'author':author,
					'author_location':author_location,
					'friend_count':friend_count,
					'author_reviews_count':author_reviews_count,
					'photo_count':photo_count,
					'url':url,
					'author_page':raw_review_author_link
			}
		scraped_data.append(data)
	return scraped_data
if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('url',help = 'yelp bussiness url')
	sort_help_text="""Avilable sort orders are: 
	date_desc,
	date_asc,
	rating_desc,
	rating_asc
	"""
	argparser.add_argument('sort',help = sort_help_text)
	args = argparser.parse_args()
	url = args.url
	sort = args.sort
	yelp_url = url.split('?')[0]+"_sort_by="+sort
	scraped_data = parse(url)
	yelp_id = yelp_url.split('/')[-1]

	with open("reviews-%s.csv"%(yelp_id),'w')as csvfile:
		fieldnames = ['review_date','review_rating','review_content','useful_count','funny_count','cool_count','author','author_location','author_reviews_count','photo_count','friend_count','url','author_page']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames,lineterminator='\n')
		writer.writeheader()
		for row in  scraped_data:
			writer.writerow(row)