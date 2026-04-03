import scrapy

class MensaSpider(scrapy.Spider):
  name = "frank"
  start_urls = ["https://www.imensa.de/index.html"]

    
  def parse (self, response):
    # get next page for a depth first approach (go deeper)
    next_pages = response.css('a.primary::attr(href)').getall() # returns list

    # go deeper if possible
    if len(next_pages) >= 1: 
      for page in next_pages:
        page = response.urljoin(page)
        yield scrapy.Request(page, callback=self.parse)

    else: # it IS the last child:
      yield {
        "name": response.css("h1.aw-title-header-title::text").get(),
        # "federalState": response.css("h1.aw-title-header-title"),
        "location": response.css(".panel-body::text").getall()[0],
        "city": response.css(".panel-body::text").getall()[1],
        "rating_average": response.css(".aw-ratings-average::text").get(),
        "rating_count": response.css(".aw-ratings-count::text").get()
      }

      # does not write to correct output for some reason (or any output whatsoever)
