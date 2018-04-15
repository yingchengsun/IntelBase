# -*- coding: utf-8 -*-
'''
Created on Nov 5, 2017

@author: yingc
'''

from wechatsogou.api import WechatSogouAPI


ws_api = WechatSogouAPI(captcha_break_time=3)


ws_api = WechatSogouAPI()

ws_api = WechatSogouAPI(captcha_break_time=3)


ws_api = WechatSogouAPI(proxies={
    "http": "127.0.0.0.1:8888",
    "https": "127.0.0.0.1:8888",
})
ws_api =WechatSogouAPI()

result= ws_api.search_article('凯斯西储cssa')
print str(result[0]['article']).decode('unicode-escape')

'''
for key, value in result[0].items():
    print key, value
'''
