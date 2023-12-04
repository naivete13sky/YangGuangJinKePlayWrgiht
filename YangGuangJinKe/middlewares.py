# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from pyppeteer import launch
import base64,json,time
import sys
import os
sys.path.append(os.path.dirname(__file__))
import gl as gl
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
import pyppeteer
import asyncio

from scrapy.http import HtmlResponse

pyppeteer.DEBUG = False


class YangGuangJinKeDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        print("Init downloaderMiddleware use pypputeer.")
        # os.environ['PYPPETEER_CHROMIUM_REVISION'] = '588429'
        # pyppeteer.DEBUG = False
        # print(os.environ.get('PYPPETEER_CHROMIUM_REVISION'))

        loop = asyncio.get_event_loop()

        # print("*" * 30, "log in", "*" * 30)
        task = asyncio.ensure_future(self.login('wangyufeng-wwyg', 'Cc123456*', 'https://osms-web-prd.hyan-tech.com/#/login'))
        # task = asyncio.ensure_future(self.login('weijun-wwyg', 'Wj~202181', 'https://osms.sinosig.com/#/login'))
        # task = asyncio.ensure_future(self.login('fengtaozhao-wwyg', 'Ftz123...', 'https://osms.sinosig.com/#/login'))
        print("*" * 30, "log in finish", "*" * 30)
        # print("*" * 30, "task:",task, "*" * 30)
        loop.run_until_complete(task)

        # self.browser = task.result()
        print("*"*30,"init finish","*"*30)


        # print(self.browser)
        # print(self.page)
        # self.page = await browser.newPage()

    async def login(self,username, password, url):
        # 'headless': False如果想要浏览器隐藏更改False为True
        self.browser = await launch({'headless': False, 'args': ['--no-sandbox']})

        self.page = await self.browser.newPage()
        await self.page.setUserAgent('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
        await self.page.goto(url)
        await self.page.type(gl.css_login_user, username) # 输入用户名
        await self.page.type(gl.css_login_pwd, password)# 输入密码
        #获取验证码，先找到图片，再保存到本地
        html_content = await self.page.content()
        soup = BeautifulSoup(html_content, 'html.parser')

        # mask_code_png_src_all = soup.find_all('img')
        # for each in mask_code_png_src_all:
        #     print(each)

        mask_code_png_src = soup.find_all('img')[1].get('src')
        encode_img = mask_code_png_src.split(',')[1]
        with open("web.png", 'wb') as f:
            f.write(base64.b64decode(encode_img))
            f.close()
        mask_code=input("请输入验证码：")# 输入验证码
        await self.page.type(gl.css_login_mask_code, mask_code)
        await self.page.click('#app > div > div.login-panel > div > button')#点击登录
        time.sleep(3)
        return self.page



    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(self.usePypuppeteer(request))
        loop.run_until_complete(task)
        # return task.result()
        return HtmlResponse(url=request.url, body=task.result(), encoding="utf-8", request=request)

    async def usePypuppeteer(self, request):
        print('request.url:',request.url)

        #在打开正常页面地址前，先打开下面这个页面的目的是使得每次搜索前先恢复到原始状态。
        await self.page.goto('https://osms-web-prd.hyan-tech.com/#/outsourceOwnQueue')
        await asyncio.sleep(1)

        await self.page.goto(request.url)
        await asyncio.sleep(3)

        #如果是“当前案件为投诉案件，请谨慎催收！”情况。要点击弹窗提示。
        response = await self.page.content()
        # print("response:",response)
        soup = BeautifulSoup(response, 'lxml')
        current_toushuanjian_s = soup.select('#app > div > div > section > div.nav-tabs.el-tabs.el-tabs--top > div.el-tabs__content > div.containter > div.el-dialog__wrapper.settleDialog > div > div.el-dialog__body > span')
        # print("current_toushuanjian_s length:",len(current_toushuanjian_s))
        if len(current_toushuanjian_s) == 1:
            print("current_toushuanjian_s length:", len(current_toushuanjian_s))
            current_toushuanjian = soup.select('#app > div > div > section > div.nav-tabs.el-tabs.el-tabs--top > div.el-tabs__content > div.containter > div.el-dialog__wrapper.settleDialog > div > div.el-dialog__body > span')[0].text
            print("current_toushuanjian:",current_toushuanjian)
            await self.page.click('#app > div > div > section > div.nav-tabs.el-tabs.el-tabs--top > div.el-tabs__content > div.containter > div.el-dialog__wrapper.settleDialog > div > div.el-dialog__footer > span > button')


        #鼠标滚动到底
        await self.page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
        await asyncio.sleep(3)
        # content = await self.page.content()
        #下面是把身份证变成没有*。点击身份证号前面的放大镜。
        response=await self.page.content()
        soup = BeautifulSoup(response, 'lxml')
        current_sfzh_cc = soup.select(
            '#app > div > div > section > div.el-tabs.el-tabs--top > div.el-tabs__content > div.containter > div.row-content.el-row.is-justify-space-between.el-row--flex > div.el-col.el-col-18 > div > div.carousel1.el-carousel.el-carousel--horizontal > div > div.el-carousel__item.is-active.is-animating > div > div > div:nth-child(4) > div:nth-child(1) > div > span')[
            0].text
        if len(current_sfzh_cc) == 11:
            print("find 11 sfzh!身份证号被数据脱敏了，需要点击得到明文身份证号！")
            time.sleep(1)
            await self.page.click('#app > div > div > section > div.nav-tabs.el-tabs.el-tabs--top > div.el-tabs__content > div.containter > div.row-content.el-row.is-justify-space-between.el-row--flex > div.el-col.el-col-18 > div > div.carousel1.el-carousel.el-carousel--horizontal > div > div.el-carousel__item.is-active.is-animating > div > div > div:nth-child(4) > div:nth-child(1) > div > i')#点击获取明文身份证号
            time.sleep(1)
        else:
            print('sfzh len:',len(current_sfzh_cc))
        content = await self.page.content()
        # print("*"*100,content)
        return content

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
