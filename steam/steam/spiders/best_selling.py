import scrapy
from ..items import SteamItem
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
import json


class BestSellingSpider(scrapy.Spider):
    name = 'best_selling'
    allowed_domains = ['store.steampowered.com']
    count = 50
    start_position = 0
    start_urls = [
        f'https://store.steampowered.com/search/results/?query&start={start_position}&count={count}&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1']

    def parse(self, response):
        parsed_data = json.loads(response.body)
        html = parsed_data['results_html']
        sel = Selector(text=html)
        games = sel.xpath("//a")

        for game in games:
            loader = ItemLoader(item=SteamItem(), selector=game, response=response)
            loader.add_xpath('game_url', ".//@href")
            loader.add_xpath('img_url', ".//div[@class='col search_capsule']/img/@src")
            loader.add_xpath('game_name', ".//span[@class='title']/text()")
            loader.add_xpath('release_date', ".//div[@class='col search_released responsive_secondrow']/text()")
            loader.add_xpath('platforms', ".//span[contains(@class, 'platform_img') or @class='vr_supported']/@class")
            loader.add_xpath('reviews_summary', ".//span[contains(@class, 'search_review_summary')]/@data-tooltip-html")
            loader.add_xpath('discount_rate', ".//div[@class='col search_discount responsive_secondrow']/span/text()")
            loader.add_xpath('original_price', ".//div[@class='col search_price_discount_combined responsive_secondrow']")
            loader.add_xpath('discount_price', ".//div[contains(@class, 'discounted')]/text()")
            yield loader.load_item()

        if self.start_position < parsed_data['total_count']:
            self.start_position += self.count
            yield scrapy.Request(
                url=f'https://store.steampowered.com/search/results/?query&start={self.start_position}&count={self.count}&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1',
                method="GET",
                callback=self.parse)
