# -*- coding:utf-8 -*-
'''
Created on Apr 16, 2018

@author: yingc
'''
import logging
 
def t():
    logger.info('dddd')  
    
if __name__ == "__main__":
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
     
    # create a file handler
     
    handler = logging.FileHandler('hello.log')
    handler.setLevel(logging.INFO)
     
    # create a logging format
     
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
     
    # add the handlers to the logger
     
    logger.addHandler(handler)
     
    logger.info('Hello baby')
    t()
