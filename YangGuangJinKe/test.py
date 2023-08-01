import time
import gl as gl
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import base64,json
import asyncio
from pyppeteer import launch

class Yg():
    pass
    async def login(self,username, password, url):
        # 'headless': False如果想要浏览器隐藏更改False为True
        self.browser = await launch({'headless': True, 'args': ['--no-sandbox']})
        self.page = await self.browser.newPage()
        await self.page.setUserAgent('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
        await self.page.goto(url)
        await self.page.type(gl.css_login_user, username) # 输入用户名
        await self.page.type(gl.css_login_pwd, password)# 输入密码
        #获取验证码，先找到图片，再保存到本地
        html_content = await self.page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        mask_code_png_src = soup.find_all('img')[4].get('src')
        encode_img = mask_code_png_src.split(',')[1]
        with open("web.png", 'wb') as f:
            f.write(base64.b64decode(encode_img))
            f.close()
        mask_code=input("请输入验证码：")# 输入验证码
        await self.page.type(gl.css_login_mask_code, mask_code)
        await self.page.click('#app > div > div.login-panel > div > button')#点击登录
        time.sleep(3)

    async def get_by_name(self,name):



        # time.sleep(50)
        await self.page.type(gl.css_search_name, name)#输入要搜索的客户姓名
        await self.page.click(gl.css_search)#点击搜索用户名
        # print(await page.cookies())
        time.sleep(1.7)
        html_content=await self.page.content()
        df=pd.read_html(html_content)
        df=df[1]
        bdh=df.values[0][7]
        sfzh=df.values[0][10]
        # print(bdh,sfzh)
        url_detail='https://osms-web-prd.hyan-tech.com/#/caseDetails?policyCode={0}&name={1}'.format(bdh,name)

        await self.page.goto(url_detail)
        time.sleep(2.5)
        html_content=await self.page.content()
        # print(html_content)
        df = pd.read_html(html_content)
        # print(df)
        my_df = df[4]
        # print(my_df)

        print('{0}的联系方式纪录数'.format(name), len(my_df))

        # time.sleep(100)
        # 本人手机号
        br_mobile = my_df[(my_df[2] == "本人") & (my_df[3] == "移动电话")].values[0][0]

        # 配偶姓名
        try:
            pe_name = my_df[(my_df[2] == "配偶") & (my_df[3] == "移动电话")].values[0][1]
        except:
            pe_name = ""

        # 配偶手机号
        try:
            pe_mobile = my_df[(my_df[2] == "配偶") & (my_df[3] == "移动电话")].values[0][0]
        except:
            pe_mobile = ""

        # 家人姓名
        try:
            jr_name = my_df[(my_df[2] == "兄弟") & (my_df[3] == "移动电话")].values[0][1]
        except:
            jr_name = ""

        # 家人手机号
        try:
            jr_mobile = my_df[(my_df[2] == "兄弟") & (my_df[3] == "移动电话")].values[0][0]
        except:
            jr_mobile = ""

        # 同事姓名
        try:
            ts_name = my_df[(my_df[2] == "同事") & (my_df[3] == "移动电话")].values[0][1]
        except:
            ts_name = ""

        # 同事手机号
        try:
            ts_mobile = my_df[(my_df[2] == "同事") & (my_df[3] == "移动电话")].values[0][0]
        except:
            ts_mobile = ""



        # 创建一条记录
        new = pd.DataFrame({'姓名': name,
                            '保单号': bdh,
                            '身体证号码': sfzh,
                            '本人手机号': br_mobile,
                            '配偶': pe_name,
                            '配偶手机号': pe_mobile,
                            '家人': jr_name,
                            '家人手机号': jr_mobile,
                            '同事': ts_name,
                            '同事手机号': ts_mobile,
                            }, index=[1]
                           )  # 自定义索引为：1 ，这里也可以不设置index

        print(new.values[0])
        conn = sqlite3.connect("my.db")
        new.to_sql("cc", conn, if_exists='append', index=False)
        # 恢复一下，为下次搜索准备好
        await self.page.goto(gl.url_search)
        await self.page.click(gl.css_search_clear)
        # time.sleep(1)

async def main(url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setViewport(viewport={'width': 1366, 'height': 768})
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3494.0 Safari/537.36')

    # 是否启用js
    await page.setJavaScriptEnabled(enabled=True)

    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')  # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate(
        '''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate(
        '''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    await page.goto(url,options={'timeout': 5000})

    # await asyncio.sleep(5)
    # 打印页面文本
    return await page.content()


if __name__ == '__main__':
    df_name = pd.read_excel("name.xlsx")
    yg=Yg()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(yg.login('wangyufeng-wwyg', 'Cc123456*', 'https://osms-web-prd.hyan-tech.com/#/login'))
    for each in range(0, len(df_name)):
        name=(df_name.iloc[[each], [0]].values[0][0])
        loop.run_until_complete(yg.get_by_name(name))

    tlist = ["https://www.baidu.com/",
             ]

    task = [main(url) for url in tlist]

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*task))
    for res in results:
        print(res)

