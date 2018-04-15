#coding:utf-8
from lxml import html  
import json
import requests
from exceptions import ValueError
from time import sleep
import MySQLdb
from collections import OrderedDict

def parse(url,ASIN):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url,headers=headers)

    for i in range(20):
        sleep(1)
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
          
            XPATH_IMAGE_LINK= '//span[@class="a-list-item"]//img/@data-old-hires'
            RAw_IMAGE_LINK = doc.xpath(XPATH_IMAGE_LINK)
             
         
            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)

 
            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
 
            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE
            #retrying in case of caotcha
            if not NAME :
                raise ValueError('captcha')

            data = {
                    'ASIN':ASIN,
                    'NAME':NAME,
                    'SALE_PRICE':SALE_PRICE,
                    'ORIGINAL_PRICE':ORIGINAL_PRICE,
                    'AVAILABILITY':AVAILABILITY,
                    'CATEGORY':CATEGORY,
                    'URL':url,
                    'IMAGE':RAw_IMAGE_LINK[0],
                    }
 
            return data
        except Exception as e:
            print e
 
def ReadAsin():
    # AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))
    '''
    'B01BI2VZEI' #6
    'B00YD54GG2' #6 plus
    'B00YD53JRO' #5c
    'B00ASURUYQ' #5
    'B01N9YOF3R' #7
    'B075QJSQLH' #8
    'B075QN8NDH' #X
    'B01MQHADBT' #Lenovo 
    'B01MQTJXWZ' #Lenovo
    'B073W5LDKM' #Dell Inspiron
    'B01N8U0046' #HP
    'B074HDDH7B' #HP
    'B015WXL0C6' #MacBook Air 
    'B072QGG3V7' #MacBook
    '''
    
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
    
    #AsinList = ['B00ASURUYQ']
    extracted_data = []
    for i in AsinList:
        url = "http://www.amazon.com/dp/"+i
        print "Processing: "+url
        extracted_data.append(parse(url,i))
        sleep(1)
    f=open('product.json','w')
    #json.dump(extracted_data,f,indent=4)
    json.dump(extracted_data,f)
    f.close()
    
    try:
        # Access to MySQLdb
        conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='',port=3306,charset='utf8')
        cur=conn.cursor()
        # If doesn't already exist, create schema and table
        #cur.execute('create database if not exists intelbase')
        conn.select_db('intelbase')
        cur.execute('create table if not exists amazon_product (ASIN varchar (20) not null primary key, NAME varchar(60), SALE_PRICE varchar(20),\
        ORIGINAL_PRICE varchar(20), AVAILABILITY varchar(20), CATEGORY varchar(60), URL varchar(50), IMAGE varchar(100) )\
        DEFAULT CHARSET=utf8 ')
    
        # Enter json-file  
        fileHandle=file('product.json')
        fileList = fileHandle.readlines()
        #OrderedDict: keep the order of dictionary data read from json same as the original order
        print fileList
        dictinfo = json.loads(fileList[0],object_pairs_hook=OrderedDict)
        
            # Iterate through json-file
        for test_record in dictinfo:
            '''
            record_list=[]
            for record_value in test_record.values():
            # Transfer the coding type 'unicode' to utf8 and store records in list
                if (type(record_value)==unicode):
                    record_value=record_value.encode('utf-8')
                record_list.append(record_value)
            # If there are some values missed in the final line, append "null" values
            while(len(record_list)<7):
                record_list.append('')
            '''
            # Insert records in MySQL 
            cur.execute('replace into amazon_product values(%s,%s,%s,%s,%s,%s,%s,%s)',
                        (test_record['ASIN'],test_record['NAME'],test_record['SALE_PRICE'],test_record['ORIGINAL_PRICE'],test_record['AVAILABILITY'],
                         test_record['CATEGORY'],test_record['URL'],test_record['IMAGE']))
            conn.commit()
        
        cur.close()
        conn.close()
        fileHandle.close()
        print len(dictinfo),'records have been inserted successfully!'
    
        # If error occurs while inserting records
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == "__main__":
    ReadAsin()