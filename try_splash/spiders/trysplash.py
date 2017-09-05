# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class TrySplashSpider(scrapy.Spider):
    name = 'try_splash'
    start_urls = ['https://www.flyeralarm.com/uk/shop/configurator/index/id/5625/standard-business-cards.html']

    lua = """
function main(splash)
  splash.private_mode_enabled = false
  splash:go(splash.args.url)
  splash:wait(0.5)
  splash:set_viewport_full()
  local el = assert(splash:select("div.attributeValue"))
  assert(el:mouse_click())
  splash:wait(1)
  local el1 = assert(splash:select("div.attributeValue"))
  return {div = el1:png(),
          html = splash:html(),
          picture = splash:png(1024, 1024),
          t = el1:text()
         }
end
    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                endpoint='execute',
                args={'lua_source': self.lua, 'wait': 2},
            )

    def parse(self, response):
        puk = 1
        print(response.data.get('t'))
        pass
        # sometimes Splash does not work for the first time )))
        # response.body is a result of render.html call; it
        # contains HTML processed by a browser.
        # response.data
