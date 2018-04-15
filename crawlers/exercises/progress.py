'''
Created on Dec 4, 2017

@author: yingc
'''
import urllib
def cbk(number, block, size):  
    '''回调函数 
    @a: 已经下载的数据块 
    @b: 数据块的大小 
    @c: 远程文件的大小 
    '''  
    print number, block, size
    per = 100.0 * number * block / size  
    if per > 100:  
        per = 100  
    print '%.2f\r' % per
    #print per
url = 'http://www.cnn.com'
local = 'd://google.html'
urllib.urlretrieve(url, local, cbk)