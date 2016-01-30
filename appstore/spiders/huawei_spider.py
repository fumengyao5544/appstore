import scrapy
import re
from scrapy.selector import Selector
from appstore.items import AppstoreItem

class HuaweiSpider(scrapy.Spider):
  name = "huawei"
  allowed_domains = ["huawei.com"]

  start_urls = [
    "http://appstore.huawei.com/more/all"
]

  #Extract urls from homepage
  def parse(self, response):
    page = Selector(response)

    '''
    divs = page.xpath('//div[@class="game-info  whole"]')

    for div in divs:
      item = AppstoreItem()

      item['title'] = div.xpath('.//h4[@class="title"]/a/text()'). \
	  extract_first().encode('utf-8')

      item['url'] = div.xpath('.//h4[@class="title"]/a/@href').extract_first()

      appid = re.match(r'http://.*/(.*)', item['url']).group(1)
      item['appid'] = appid

      item['intro'] = div.xpath('.//p[@class="content"]/text()'). \
	  extract_first().encode('utf-8')
      yield item
    '''

    hrefs = page.xpath('//h4[@class="title"]/a/@href')
     
    for href in hrefs:
      url = href.extract()
      yield scrapy.Request(url, callback=self.parse_item)

  #Extract title, url, intro, recommended apps from the app page
  def parse_item(self, response):
    page = Selector(response)
    item = AppstoreItem()

    item['title'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()'). \
	extract_first().encode('utf-8')
    item['url'] = response.url
    item['appid'] = re.match(r'http://.*/(.*)', item['url']).group(1)
    item['intro'] = page.xpath('//meta[@name="description"]/@content').extract_first().encode('utf-8') 
    item['thumbnailurl'] = page.xpath('//ul[@class="app-info-ul nofloat"]/li[@class="img"]/img[@class="app-ico"]/@lazyload').extract_first()

    divs = page.xpath('//div[@class="open-info"]')
    recomm = ""
    #Extract list information of recommended apps
    for div in divs:
      url = div.xpath('./p[@class="name"]/a/@href').extract_first()
      recommended_appid = re.match(r'http://.*/(.*)',url).group(1)
      name = div.xpath('./p[@class="name"]/a/text()').extract_first().encode('utf-8')
      recomm += "{0}:{1},".format(recommended_appid, name)
    item['recommended'] = recomm
    yield item
