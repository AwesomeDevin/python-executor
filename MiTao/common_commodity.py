#coding:utf-8

import sys
import thread
reload(sys)
sys.setdefaultencoding('utf-8')


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import urllib2
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
from selenium.webdriver import ChromeOptions
import mongodb_api
import os
import time

CURRENT_DIR = os.getcwd()
CHROMEDRIVER_DIR = os.path.join(CURRENT_DIR, "bin", "chromedriver.exe")
options = ChromeOptions()
browser = webdriver.Chrome(executable_path=CHROMEDRIVER_DIR,options=options)
# browser = webdriver.Firefox()

wait = WebDriverWait(browser,10)
hca = mongodb_api.CommonCommodityAPI()
# key = '长裙'


class MultipleSpider:

    def __init__(self,kind):
        self.type = kind.decode('gbk')
        # self.url = 'https://s.taobao.com/search?q='
        self.MAX_PAGE = 3
        self.cur_page = 1
        # hca = HotCommodityAPI()
    def index_page(self,page):
        print(u"正在爬取第",page,u"页",self.type)
        try:
            url = 'https://s.taobao.com/search?q={}'.format(self.type)
            # url = 'https://s.taobao.com/search'
            # print url
            time.sleep(5)
            data = browser.get(url)
            
            if page>1 :
                input = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
                time.sleep(5)
                submit = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
                input.clear()
                print('input')
                input.send_keys(page)

                time.sleep(5)
                print('click')
                submit.click()
            wait.until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
            time.sleep(5)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
            self.get_products()
        except TimeoutException:
            self.index_page(page)


    def get_products(self):
        """
        提取商品数据
        """
        index = 1
        html = browser.page_source
        doc = pq(html)
        items = doc('#mainsrp-itemlist .items .item').items()
        
        for item in items:
            product = {
                'image': item.find('.pic .img').attr('data-src'),
                'price': item.find('.price').text(),
                'deal': item.find('.deal-cnt').text(),
                'title': item.find('.title').text(),
                'shop': item.find('.shop').text(),
                'location': item.find('.location').text(),
                'show':True,
                'type':self.type,
            }
            self.save_to_mongo(product)
            index += 1
            # print(index+1)
            # print index
        print(index)
        self.cur_page  = self.cur_page + 1
        if self.cur_page > self.MAX_PAGE:
            browser.close()
            pass
        else:
            self.index_page(self.cur_page)


    def save_to_mongo(self,product):
        try:
            # print(product['shop'])
            hca.add_commodity_info(product)
        except Exception,e:
            print('保存失败')


    def main(self):
        # for i in range(1,self.MAX_PAGE):
            # thread.start_new_thread(self.index_page, (1,))
            # print i
            hca.remove_commodity_info(self.type)
            self.index_page(self.cur_page)



# print sys.argv[1]
ms = MultipleSpider(sys.argv[1])
try:
    ms.main()
except Exception,e:
    print '请求出错'
    ms.main()
# hca.add_commodity_info({'shop':'123'})






