'''
Created on Dec 4, 2017

@author: yingc
'''
import os
import urllib

import re
import threading
import urllib2
from bs4 import BeautifulSoup  

class QsSpider:
    def __init__(self):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.header = {'User-Agent': self.user_agent}
        self.save_dir = './pic'
        # ��ַ
        self.url = 'http://tieba.baidu.com/p/2460150866'
        #self.url = 'https://www.zhihu.com/question/36390957'
        # ��Ҫ��ȡ��ҳ����
        self.page_num = 10

    def start(self):
        self.load_html()
        '''
        for i in range(1, self.page_num):
            # ÿ��ҳ�洴��һ���߳�ȥ����
            thread = threading.Thread(target=self.load_html, args=str(i))
            thread.start()
        '''

    def load_html(self, page=1):
        # ��ȡ��վ��htmlҳ��
        try:
            #web_path = self.url % page
            web_path = self.url
            request = urllib.urlopen(web_path).read()
            #html_content = request.decode('gb2312')
            html_content = request
            #print(html_content)
            self.pick_pic(html_content)
        except urllib.ftperrors() as e:
            print(e)
        return

    def save_pic(self, img):
        # ����ͼƬ��ִ��·����picĿ¼�£��滻������Ϊ�ļ����������ַ�
        save_path = self.save_dir + "/" + img.replace(':', '@').replace('/', '_')
        # ���Ŀ¼�����ھʹ���
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        # ��ӡ·����ִ�е��߳�
        print(save_path + '---%s' % threading.current_thread())
        # ȡ��ͼƬ��·�������ļ������浽ָ��Ŀ¼��
        urllib.urlretrieve(img, save_path)
        pass

    def pick_pic(self, html_content):
        # ����ƥ���ͼƬ����
        #regex = r'src="(http:.*?\.(?:jpg|png|gif))'
        '''
        regex = r'src="(.+?\.jpg)" pic_ext'
        patten = re.compile(regex)
        soup=BeautifulSoup(respond)#ʵ����һ��BeautifulSoup���� 
        pic_path_list = patten.findall(html_content)
        for i in pic_path_list:
            self.save_pic(str(i))
        '''
        
        soup=BeautifulSoup(html_content)#ʵ����һ��BeautifulSoup����
        #f=open('tieba.txt','w') 
        #f.write(soup.prettify().encode('utf-8'))
        #f.close()

        #lst=[]#����list����  
          
        for link in soup.find_all(class_='l_post l_post_bright j_l_post clearfix '): 
            print link.div
            #address=link.get('src')#��ȡ��ǩ����Ϊdata-original�����ݣ���ͼƬ��ַ 
            #print address 
            #self.save_pic(str(address)) 
    
spider = QsSpider()
spider.start()