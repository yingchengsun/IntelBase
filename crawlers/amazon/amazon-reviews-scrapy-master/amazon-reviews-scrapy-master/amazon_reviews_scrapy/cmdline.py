# - * - coding: UTF-8 - * - 
'''
Created on Nov 21, 2017

@author: yingc
'''
import scrapy.cmdline

if __name__ =='__main__':
    scrapy.cmdline.execute(argv = ['scrapy','crawl','amazon-reviews-spider','-a','product_id=B002QQ8H8I'])
    #scrapy.cmdline.execute(argv = ['scrapy','crawl','facebook_post','-a', 'target_username=bbctech','-o', 'bbctech.json'])
 