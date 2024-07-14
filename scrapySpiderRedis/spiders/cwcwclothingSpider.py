"""_summary_
运行该脚本需要mysql环境，配置settings.py，需要导入otherDemoCodeTest下面cwcwclothingSpider.sql文件
Yields:
    _type_: _description_
"""
from typing import Iterable
from scrapy import Request
from scrapySpiderRedis.items import ScrapyspiderRedisItem
import scrapy
from bs4 import BeautifulSoup
import re
import time
import requests
from scrapySpiderRedis.log import Logging
# from scrapy.spidermiddlewares.httperror import HttpError
# from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
# dont_filter=True 表示不走重新爬取流程

class CwcwclothingspiderSpider(scrapy.Spider):
    name = "cwcwclothingSpider"
    allowed_domains = ["cwcwclothing.com","baidu.com"]
    # start_urls = ["https://cwcwclothing.com"]
    start_urls="https://cwcwclothing.com/collections/grace-mila"
    logger = Logging("cwcwclothingSpider.log").get_logger() # 使用自定义日志器

    cookies = {
        'secure_customer_sig': '',
        'localization': 'GB',
        'cart_currency': 'GBP',
        '_tracking_consent': '%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22CNZJ%22%2C%22reg%22%3A%22%22%7D',
        '_cmp_a': '%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%7D',
        '_shopify_y': 'b8b7e79a-b3fb-4527-9044-57a7f0f3f85a',
        '_orig_referrer': '',
        '_landing_page': '%2Fcollections%2Fgrace-mila',
        'receive-cookie-deprecation': '1',
        '_shopify_sa_p': '',
        'shopify_pay_redirect': 'pending',
        'keep_alive': '22c4ce70-1eee-4173-a7a1-421f60ac3927',
        '_shopify_s': '809968be-f34a-4228-a097-12d0d52d5d3f',
        '_shopify_sa_t': '2024-06-20T12%3A00%3A59.537Z',
        'qab_previous_pathname': '/collections/coats',
    }

    def start_requests(self) -> Iterable[Request]:
        """_summary_
        爬虫开始
        Returns:
            Iterable[Request]: _description_
        """
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': 'secure_customer_sig=; localization=GB; cart_currency=GBP; _tracking_consent=%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22CNZJ%22%2C%22reg%22%3A%22%22%7D; _cmp_a=%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%7D; _shopify_y=b8b7e79a-b3fb-4527-9044-57a7f0f3f85a; _orig_referrer=; _landing_page=%2Fcollections%2Fgrace-mila; receive-cookie-deprecation=1; _shopify_sa_p=; shopify_pay_redirect=pending; keep_alive=22c4ce70-1eee-4173-a7a1-421f60ac3927; _shopify_s=809968be-f34a-4228-a097-12d0d52d5d3f; _shopify_sa_t=2024-06-20T12%3A00%3A59.537Z; qab_previous_pathname=/collections/coats',
            'if-none-match': '"cacheable:65d53ddaa61c30f7ce0ea8f63bebedc3"',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }
        # yield Request(url=self.sort_link_url,headers=headers,cookies=cookies,callback=self.parse_sort_links,meta={'source_list': response.url})
        yield Request(url=self.start_urls,headers=headers,cookies=self.cookies,callback=self.parse_sort_links,dont_filter=True) # dont_filter=True表示该域名不走过滤器

    def parse_sort_links(self,response):
        """_summary_
        解析 列表页链接
        Args:
            response (_type_): _description_
        """
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': 'secure_customer_sig=; localization=GB; cart_currency=GBP; _tracking_consent=%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22CNZJ%22%2C%22reg%22%3A%22%22%7D; _cmp_a=%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%7D; _shopify_y=b8b7e79a-b3fb-4527-9044-57a7f0f3f85a; _orig_referrer=; _landing_page=%2Fcollections%2Fgrace-mila; receive-cookie-deprecation=1; _shopify_sa_p=; shopify_pay_redirect=pending; keep_alive=46a6144f-0309-4250-ad19-3c663805aee6; _shopify_s=809968be-f34a-4228-a097-12d0d52d5d3f; _shopify_sa_t=2024-06-20T12%3A13%3A50.106Z; qab_previous_pathname=/collections/coats/products/nice-things-waterproof-hooded-trench-coat-dark-yellow',
            'if-none-match': '"cacheable:40c8c0a1f5d4911961e39e663a189d43"',
            'priority': 'u=0, i',
            'referer': 'https://cwcwclothing.com/collections/grace-mila',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }
        soup = BeautifulSoup(response.text, 'html.parser')
        href_value = soup.find_all('a', class_='mobile-nav__sublist-link', href=True)
        sort_list = ["https://cwcwclothing.com" + href["href"] for href in href_value]
        for sort_link in sort_list:
            yield Request(url=sort_link,headers=headers,cookies=self.cookies,callback=self.parse_data_links,meta={"sort_url":sort_link})

    def parse_data_links(self,response):
        """_summary_
        解析列表页地址
        Args:
            response (_type_): _description_
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }

        soup = BeautifulSoup(response.text, 'html.parser')
        href_value = soup.find_all('a', class_='grid-view-item__link grid-view-item__image-container full-width-link', href=True)
        data_list = ["https://cwcwclothing.com" + href["href"] for href in href_value ]
        self.logger.info(f"==================解析详情页页地址是{data_list[0:3]}==================")
        self.logger.info(f"==================解析meta地址是{response.meta}==================")
        for data_url in data_list:
            self.logger.info(f"{data_url}")
            self.logger.info(requests.get(url=data_url).status_code)
            yield Request(url=data_url,headers=headers,callback=self.parse_data_list,meta=response.meta)

    def parse_data_list(self,response):
        """_summary_
        解析详情页
        Args:
            response (_type_): _description_
        """
        self.logger.info("++++++++++++++++++++++++++++++++++")
        self.logger.info(response.text[0:10])
        self.logger.info("++++++++++++++++++++++++++++++++++")
        item = ScrapyspiderRedisItem() # 实例化一个数据库对象
        resp=response.text
        soup = BeautifulSoup(resp, 'html.parser')
        self.logger.info(f"详情页内容是{resp[0:20]}")
        self.logger.info(f"meta内容是{response.meta}")
        title = re.search(r'<meta property="og:title" content="(.*?)">', resp).group().split('"')[-2]
        price = re.search(r'<meta property="og:price:amount" content="(.*?)">', resp).group().split('"')[-2]
        sorts = response.meta["sort_url"].split("/")[-1]
        des = re.search(r'<meta property="og:description" content="(.*?)">', resp).group().split('"')[-2]
        sizes = ""
        for size in soup.find('select', class_='product-form__variants no-js', id=True).find_all('option'):
            sizes += size.text + "|"
        imgs = ""
        for img in soup.find_all('img', class_='product-single__thumbnail-image', src=True):
            imgs += "https:" + img["src"] + "|"

        item["title"] = title
        item["sort"] = sorts
        item["num"] = ""
        item["price"] = price
        item["size"] = sizes[:-1]
        item["color"] = ""
        item["color_img"] = ""
        item["intro"] = des
        item["main_img"] = imgs[:-1]
        item["detail_img"] = ""
        item["sale"] = ""
        item["talk"] = ""
        item["mark"] = ""
        item["seo_title"] = ""
        item["seo_intro"] = ""
        item["seo_key"] = ""
        item["link"] = ""

        yield item
