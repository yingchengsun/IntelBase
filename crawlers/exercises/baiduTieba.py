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
        # 网址
        self.url = 'http://tieba.baidu.com/p/2460150866'
        #self.url = 'https://www.zhihu.com/question/36390957'
        # 需要爬取的页面数
        self.page_num = 10

    def start(self):
        self.load_html()
        '''
        for i in range(1, self.page_num):
            # 每个页面创建一个线程去下载
            thread = threading.Thread(target=self.load_html, args=str(i))
            thread.start()
        '''

    def load_html(self, page=1):
        # 获取网站的html页面
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
        # 保存图片到执行路径的pic目录下，替换不能作为文件名的特殊字符
        save_path = self.save_dir + "/" + img.replace(':', '@').replace('/', '_')
        # 如果目录不存在就创建
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        # 打印路径及执行的线程
        print(save_path + '---%s' % threading.current_thread())
        # 取回图片已路径名作文件名保存到指定目录下
        urllib.urlretrieve(img, save_path)
        pass

    def pick_pic(self, html_content):
        # 正则匹配出图片链接
        #regex = r'src="(http:.*?\.(?:jpg|png|gif))'
        '''
        regex = r'src="(.+?\.jpg)" pic_ext'
        patten = re.compile(regex)
        soup=BeautifulSoup(respond)#实例化一个BeautifulSoup对象 
        pic_path_list = patten.findall(html_content)
        for i in pic_path_list:
            self.save_pic(str(i))
        '''
        
        soup=BeautifulSoup(html_content)#实例化一个BeautifulSoup对象
        #f=open('tieba.txt','w') 
        #f.write(soup.prettify().encode('utf-8'))
        #f.close()

        #lst=[]#创建list对象  
          
        for link in soup.find_all(class_='l_post l_post_bright j_l_post clearfix '): 
            print link.div
            #address=link.get('src')#获取标签属性为data-original的内容，即图片地址 
            #print address 
            #self.save_pic(str(address)) 
    
spider = QsSpider()
spider.start()