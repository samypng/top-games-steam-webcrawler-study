# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.selector import Selector
from w3lib.html import remove_tags


def handle_review_summary(review_summary: str) -> str:
    try:
        return remove_tags(review_summary)
    except TypeError:
        return "No Review"


def handle_platform(platform: str) -> str:
    return platform.split(" ")[-1]


def handle_original_price(html: str) -> str:
    selector = Selector(text=html)
    discount_elements = selector.xpath(".//div[contains(@class, 'discounted')]")

    if len(discount_elements) > 0:
        return selector.xpath("normalize-space(.//div[contains(@class, 'discounted')]/span/strike/text())").get()
    else:
        return selector.xpath("normalize-space(.//div[@class='col search_price  responsive_secondrow']/text())").get()


def handle_discount_rate(discount_rate: str) -> str:
    if discount_rate:
        return discount_rate.lstrip("-")
    return discount_rate


def handle_discount_price(discount_price) -> str:
    if discount_price:
        return discount_price.strip()
    return discount_price


class SteamItem(scrapy.Item):
    game_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    img_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    game_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    release_date = scrapy.Field(
        output_processor=TakeFirst()
    )
    platforms = scrapy.Field(
        input_processor=MapCompose(handle_platform)
    )
    reviews_summary = scrapy.Field(
        input_processor=MapCompose(handle_review_summary),
        output_processor=TakeFirst()
    )
    original_price = scrapy.Field(
        input_processor=MapCompose(handle_original_price),
        output_processor=TakeFirst()
    )
    discount_price = scrapy.Field(
        input_processor=MapCompose(handle_discount_price),
        output_processor=TakeFirst()
    )
    discount_rate = scrapy.Field(
        input_processor=MapCompose(handle_discount_rate),
        output_processor=TakeFirst()
    )
