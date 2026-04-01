import scrapy

class MensaSpider(scrapy.Spider):
  name = "Frank"

  async def start (self):
    urls = ["https://www.imensa.de/index.html"]
    
  def parse (self, response):
    # get next page for a depth first approach (go deeper)
    next_page = response.css('a.primary::attr(href)').getAll()

    # if it's not the last child
    if next_page is not None: 
      next_page = response.urljoing(next_page)
      yield scrapy.Request(next_page, callback=self.parse)

    else: # it IS the last child:
      yield {
        "name": response.css("h1.aw-title-header-title::text").get(),
        # "federalState": response.css("h1.aw-title-header-title"),
        "location": response.css("a.panelbody::text").get(),
        "city": response.css("a.panelbody>br::after").get(),
        "rating_average": response.css("div.aw-rating-average::text").get(),
        "rating_count": response.css("div.aw-rating-count::text").get()
      }
