'''
Created on Dec 4, 2017

@author: yingc
'''
import urllib
def cbk(number, block, size):  
    '''�ص����� 
    @a: �Ѿ����ص����ݿ� 
    @b: ���ݿ�Ĵ�С 
    @c: Զ���ļ��Ĵ�С 
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