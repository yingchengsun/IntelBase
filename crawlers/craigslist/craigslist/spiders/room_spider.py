'''
Created on Nov 21, 2017

@author: yingc
'''
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re
from craigslist.items import CraigslistItem

class RoomSpider(CrawlSpider):
    name = "rooms"
    #allowed_domains = ["vancouver.craigslist.ca"]
    allowed_domains = ["http://vancouver.craigslist.ca/search/roo"]
    start_urls = ["https://vancouver.craigslist.ca/rds/roo/d/beautiful-room-in-basement/6392394422.html"]
    
    #rules = (Rule(SgmlLinkExtractor(allow=[r'.*?/.+?/roo/\d+\.html']), callback='parse_roo', follow=False),)
    
    def parse(self, response):
        print response
        url = response.url
        print url
        titlebar = response.xpath('//*[@id="pagecontainer"]/section/h2/text()').extract()
        title = ''.join(titlebar)
        price = response.xpath('//*[@class="price"]/text()').extract()
        #price = int(re.search(r'\$(\d+)', price[0]).group(1))
        price = 100
        content = response.xpath('//*[@id="postingbody"]').extract()[0]
        maplink = response.xpath('//*[@id="pagecontainer"]/section/section[2]/div[1]/div/p/small/a[1]').extract()

        longitude = None
        latitude = None
        mapdata = response.xpath('//*[@id="map"]')
        if len(mapdata) != 0:
            longitude = float(mapdata.xpath("@data-longitude").extract()[0])
            latitude = float(mapdata.xpath("@data-latitude").extract()[0])

        #attributes = response.xpath('//*[@id="pagecontainer"]/section/section[2]/div[1]/p').extract()[0]
        attributes=['good']
        image_links = response.xpath('//*[@id="thumbs"]/a/@href').extract()
        time = response.xpath('//*[@id="display-date"]/time/@datetime').extract()[0]

        item = CraigslistItem(url=url,
        size=None,
          price=price,
          title=title,
          content=content,
          maplink=maplink,
          longitude=longitude,
          latitude=latitude,
          attributes=attributes,
          image_links=image_links,
          time=time)
        
        return item
        