import os

import numpy as np
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re

driver = webdriver.Chrome()
driver.get('https://www.amazon.com/dp/B09PV758HF?th=1')
time.sleep(3)
driver.find_element(By.ID, 'glow-ingress-line2').click()
driver.implicitly_wait(5)
driver.find_element(By.ID, "GLUXZipUpdateInput").click()
driver.implicitly_wait(5)
driver.find_element(By.ID, 'GLUXZipUpdateInput').send_keys('90005')
driver.implicitly_wait(5)
ActionChains(driver).send_keys(Keys.ENTER).perform()  # 直接输入回车
driver.implicitly_wait(5)
driver.refresh()
time.sleep(3)


def get_data(s_list):
    tim_r = np.random.randint(5, size=len(s_list))
    ygsj = 0
    p = 0
    for xx in tim_r:
        ygsj += xx
    print('现在是' + time.strftime("%H:%M:%S", time.localtime()) + '\n预估总用时%d秒' % ygsj)
    out_put_df = pd.DataFrame(
        columns=['日期', '时间', 'ASIN', '规格', '价格', '卖家', '发货', 'FBA库存数量', '排名', '类目', 'QA数', '评论数', '评分', '合并ASIN',
                 'ASIN上架时间'])
    out_put_sku = []
    for sku in s_list:
        print('正常抓取第%d个产品' % (p + 1))
        driver.get('https://www.amazon.com/dp/{}?th=1'.format(sku))
        time.sleep(5)
        content = driver.page_source

        if sku in driver.current_url:
            try:
                spec = re.findall('''</label> <span class="selection">(.*?)</span>''', content, re.S)[0]
            except:
                spec = ''
            try:
                rank = re.findall('</th> <td> <span> {2}<span>#(.*?) in ', content)[0]
            except:
                rank = ''
            try:
                calog = re.findall('<span>#.*? in <a href=.*?>(.*?)</a>', content)[0]
            except:
                calog = ''
            try:
                seller = re.findall('''<a href=".*?" id="sellerProfileTriggerId">(.*?)</a>''', content)[0]
            except:
                seller = ''
            try:
                shipper = re.findall('<span class="a-size-small">(.*?)</span>', content)[0]
                if shipper == 'Amazon':
                    shipper = 'FBA'
                else:
                    shipper = 'FBM'
            except:
                shipper = ''
            try:
                stock = re.findall('a-size-medium a-color-price"> {4}Only (.*?) left in stock - order soon. {3}</span>',
                                   content)[0]
            except IndexError:
                try:
                    stock = re.findall(
                        '<div id="availability" class="a-section a-spacing-base }"> {17}<span ''class="a-size-medium a-color-success"> {4}(.*?) {3}</span>',
                        content)[0]
                except IndexError:
                    stock = '0'
            try:
                qa_count = re.findall(
                    '<a id="askATFLink" class="a-link-normal askATFLink" href="#Ask"> <span class="a-size-base"> (.*?) ''answered questions </span> </a> </span>',
                    content)[0]
            except:
                qa_count = 0
            try:
                rate_count = re.findall('acrCustomerReviewText" class="a-size-base">(.*?) ratings<', content)[1]
            except:
                rate_count = 0
            try:
                rate_star = \
                re.findall('eviewCountTextLinkedHistogram noUnderline" title="(.*?) out of 5 stars">', content)[1]
            except:
                rate_star = 0
            try:
                spec_opt = re.findall(
                    '<li id="size_name_.*?data-defaultasin="(.*?)" data-dp-url=".*?" class="swatchAvailable">', content)
            except:
                spec_opt = ''
            try:
                up_data = \
                re.findall('Date First Available </th> {2}<td class="a-size-base prodDetAttrValue"> (.*?) </td> </tr>',
                           content)[0]
            except:
                up_data = ''
            try:
                price = re.findall('a-offscreen">(.*?)<', content)[0]
            except:
                price = ''
            rq = time.strftime("%Y-%m-%d", time.localtime())
            sj = time.strftime("%H:%M:%S", time.localtime())
            t = time.time()
            out_put_df.loc[int(t)] = [rq, sj, sku, spec, price, seller, shipper, stock, rank, calog, qa_count,
                                      rate_count, rate_star, spec_opt, up_data]

            try:
                if spec_opt == '':
                    pass
                else:
                    for xx in spec_opt:
                        out_put_sku.append(xx)
            except:
                pass
        else:
            print('pass')
            pass
        p += 1
        print('%s完成' % sku)
        for i in range(5):
            print(f"倒计时{str(i)}秒\n", end="")
            # print("\b" * (len(f"倒计时{str(i)}秒") * 2), end="", flush=True)
            time.sleep(1)

    return out_put_df, out_put_sku


while True:
    path_sku = os.path.join(os.getcwd() + '\\' + 'sku_list' + '.xlsx')
    path = os.path.join(os.getcwd() + '\\' + 'amz_info' + '.xlsx')

    if not os.path.exists(path):
        print("file not exist!")
        data = pd.DataFrame(
            columns=['日期', '时间', 'ASIN', '规格', '价格', '卖家', '发货', 'FBA库存数量', '排名', '类目', 'QA数', '评论数', '评分', '合并ASIN',
                     'ASIN上架时间'])
    else:
        print("file exist!")
        data = pd.read_excel(path)

    if not os.path.exists(path_sku):
        print("SKU file not exist!")
        data_sku = pd.DataFrame(['B09SV53Z57', 'B09KRJV89C', 'B09PNGKK6B', 'B09MRMX611'], columns=['sku'])
    else:
        print("SKU file exist!")
        data_sku = pd.read_excel(path_sku)
    sku_list = data_sku['sku'].to_list()
    ss = get_data(sku_list)
    out_put_data = ss[0]
    for i in ss[1]:
        sku_list.append(i)
    sku_list = list(set(sku_list))

    data = pd.concat([data, out_put_data])
    data.to_excel(path, encoding='utf_8_sig', index=False)
    sku_df = pd.DataFrame(sku_list, columns=['sku'])
    sku_df.to_excel(path_sku, encoding='utf_8_sig', index=False)
    print('完成')
    driver.close()
    for x in range(1, 14400):
        print(f"倒计时{str(14400 - x)}秒\n", end="")
        print(f'等待进度：{round((14400 - x) / 14400 * 100, 2)} %')
        print('*' * int((14400 - x) / 14400 * 100))
        time.sleep(1)
