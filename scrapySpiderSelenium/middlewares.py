import time
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class SeleniumMiddlerware(object):
    """
    利用selenium，获取动态页面数据
    """

    # 定义一个xpath的捕获异常
    def xpathExists(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except:
            return False

    # 页面滚动按次数
    def scroll(self,num:int):
        for i in range(num):
            self.driver.execute_script(f'document.documentElement.scrollTop={(i + 1) * 1000}')
            time.sleep(1)

    def scroll_end(self):
        temp_height = 0
        while True:
            # 循环将滚动条下拉
            self.driver.execute_script("window.scrollBy(0,600)")
            time.sleep(1)
            # 获取当前滚动条距离顶部的距离
            check_height = self.driver.execute_script("return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            # 如果两者相等说明到底了
            if check_height == temp_height:
                # print("到底了")
                break
            temp_height = check_height

    def process_request(self, request, spider):

        # 判断请求是否来自第二个页面，只在第二个页面调用浏览器
        if not request.url == "https://mellyonline.com/collections/lilly-pulitzer":
            # 实例化selenium
            self.driver = webdriver.PhantomJS()
            self.driver.get(request.url)
            time.sleep(2)

            # 获取请求后得到的源码
            html = self.driver.page_source
            # 防止driver.page_source得到的源码不全
            # self.driver.execute_script("return document.documentElement.outerHTML")
            # 关闭浏览器
            self.driver.quit()

            # 构造一个请求的结果，将谷歌浏览器访问得到的结果构造成response，并返回给引擎
            response = scrapy.http.HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8')
            return response