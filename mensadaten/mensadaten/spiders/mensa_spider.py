import scrapy
import re

class MensaSpider(scrapy.Spider):
  name = "frank"
  start_urls = ["https://www.imensa.de/index.html"]

    
  def parse (self, response):
    # get next page
    next_pages = response.css('a.primary::attr(href)').getall() 

    # go deeper if possible
    if len(next_pages) >= 1: 
      for page in next_pages:
        page = response.urljoin(page)
        yield scrapy.Request(page, callback=self.parse)

    # get data from html
    else: 
      description = response.css('.aw-title-header-content>div>div::text').get()
      match = re.search(r"wird vom (?P<operator>.+?) betrieben\.", description)
      op = 'unknown'
      if match:
        op = match.group('operator')

      yield {
        "name": response.css("h1.aw-title-header-title::text").get(),
        "location": response.css(".panel-body::text").getall()[0],
        "plz": response.css(".panel-body::text").getall()[1][:5],
        "city": response.css(".panel-body::text").getall()[1][6:],
        "rating_average": response.css(".aw-ratings-average::text").get(),
        "rating_count": response.css(".aw-ratings-count::text").get(),
        "operator": op
      }
