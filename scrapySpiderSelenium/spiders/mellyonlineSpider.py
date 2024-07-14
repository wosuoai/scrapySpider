from typing import Iterable
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from scrapySpiderRedis.log import Logging
from scrapySpiderRedis.items import ScrapyspiderRedisItem
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
import re

class MellyonlinespiderSpider(scrapy.Spider):
    name = "mellyonlineSpider"
    allowed_domains = ["mellyonline.com"]
    start_url = "https://mellyonline.com/collections/lilly-pulitzer"
    logger = Logging("mellyonlineSpider.log").get_logger() # 使用自定义日志器

    # # 定义处理验证码的方法
    # def handle_captcha(self, driver):
    #     # 检查是否有验证码元素
    #     captcha = driver.find_element_by_id("captcha_image")
    #     if captcha:
    #         # 如果有验证码，使用OCR技术识别验证码，并输入答案
    #         captcha_image = captcha.get_attribute("src")
    #         captcha_text = self.ocr(captcha_image)
    #         captcha_input = driver.find_element_by_id("captcha_field")
    #         captcha_input.send_keys(captcha_text)
    #         captcha_submit = driver.find_element_by_class_name("submit")
    #         captcha_submit.click()

    # def start_requests(self):
    #     # 使用SeleniumRequest代替scrapy.Request
    #     yield SeleniumRequest(
    #         url=self.start_url,
    #         callback=self.parse_sort_urls,
    #         # 指定Selenium使用的Webdriver
    #         selenium_options={'executable_path': r'C:\Users\Administrator\.wdm\drivers\chromedriver\win64\chromedriver.exe'},
    #         # 设置Selenium等待元素加载的时间
    #         selenium_wait_time=5,
    #     )
        
    def parse_sort_urls(self,response):
        soup = BeautifulSoup(response, 'html.parser')
        sort_links = []
        sort_list = []
        for li_tag in soup.find("ul",class_="site-nav").find_all("li",class_="item dropdown"):
            sort1 = li_tag.find("span").text.replace('"','').replace('\n','').replace(' ','') + "|"
            for li_value in li_tag.find("ul",class_="site-nav-dropdown").find_all("li"):
                if li_value.find("ul"):
                    sort2 = sort1+li_value.find("span").text
                    for li in li_value.find("ul").find_all("li"):
                        sort_links.append("https://mellyonline.com" + li.find("a").get("href"))
                        sort_list.append(sort1 + sort2 + li.find("span").text)
                else:
                    sort_links.append("https://mellyonline.com" + li_value.find("a").get("href"))
                    sort_list.append(sort1 + li_value.find("span").text)
        # 将分类链接和类名一一对应
        for sort_url, sort in zip(sort_links, sort_list):
            yield scrapy.Request(url=sort_url, callback=self.parse_data_urls, meta={"sort": sort})

    def parse_data_urls(self,response):
        soup = BeautifulSoup(response.text, 'html.parser')
        data_urls = []
        for a_tag in soup.find_all('a', href=True, class_='product-grid-image'):
            data_value = a_tag.get('href')
            if data_value:
                data_urls.append("https://mellyonline.com" + data_value)
        for data_url in data_urls:
            yield scrapy.Request(url=data_url,callback=self.parse_data_list,meta={"sort": response.meta['sort']})

    def parse_data_list(self,response):
        self.logger.info("++++++++++++++++++++++++++++++++++")
        self.logger.info(response.text[0:10])
        self.logger.info("++++++++++++++++++++++++++++++++++")

        item = ScrapyspiderRedisItem()  # 实例化一个数据库对象
        resp = response.text
        soup = BeautifulSoup(resp, 'html.parser')
        self.logger.info(f"详情页内容是{resp[0:20]}")
        self.logger.info(f"meta内容是{response.meta}")

        try:
            price = re.search('<meta property="og:price:amount" content="(.*?)>', response).group(1).split('"')[-2]
            des = re.search('<meta property="og:description" content="(.*?)>', response).group(1).split('"')[-2]
            title = re.search('<meta property="og:title" content="(.*?)>', response).group(1).split('"')[-2]
            imgs = ""
            try:
                for src_tag in soup.find('div', class_='Product__SlideshowNavScroller').find_all("img"):
                    imgs += "https:" + src_tag["src"] + "|"
            except:
                img = re.search('<meta property="og:image" content="(.*?)">', response).group().split(">")[-2].split('"')[-2]
                imgs += img + "|"

            item["title"] = title
            item["sort"] = response.meta['sort']
            item["num"] = ""
            item["price"] = price
            item["size"] = ""
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
        except Exception as error:
            self.logger.error(f"出现的错误是{error}")