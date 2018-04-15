# - * - coding: UTF-8 - * - 
'''
Created on Nov 21, 2017

@author: yingc
'''
import scrapy.cmdline

if __name__ =='__main__':
    scrapy.cmdline.execute(argv = ['scrapy','crawl','TweetScraper','-a', 'query=Iphone 6'])

