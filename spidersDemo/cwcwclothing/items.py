# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapyspiderredisItem(scrapy.Item):
    """_summary_
    table 是表名
    =左边的字段就是mysql里表的字段,默认是intiCode里cwcwclothingSpider表
    Args:
        scrapy (_type_): _description_
    """
    # define the fields for your item here like:
    table="cwcwclothing"
    title=scrapy.Field()
    sort=scrapy.Field()
    num=scrapy.Field()
    local_num=scrapy.Field()
    price=scrapy.Field()
    size=scrapy.Field()
    color=scrapy.Field()
    color_img=scrapy.Field()
    local_color_img=scrapy.Field()
    intro=scrapy.Field()
    main_img=scrapy.Field()
    detail_img=scrapy.Field()
    local_main_img=scrapy.Field()
    local_detail_img=scrapy.Field()
    sale=scrapy.Field()
    talk=scrapy.Field()
    mark=scrapy.Field()
    seo_title=scrapy.Field()
    seo_intro=scrapy.Field()
    seo_key=scrapy.Field()
    link = scrapy.Field()