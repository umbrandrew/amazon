import os
import re,time,random
import numpy as np
import pandas as pd
import requests


def randHeader():
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html,*/*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36']
    header = {
        'Connection': head_connection[0],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[1],

        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]
    }
    return header

def get_res(sku):
    proxy_id = { "http": "54.167.4.138:10592"}
    cookie = {'session-id':'145-0459963-1297832','session-id-time':'2082787201l','ubid-main':'130-3846316-5053615','lc-main':'en_US','s_vnum':'2052117870993%26vn%3D1','s_nr':'1620117872688-New','s_dslv':'1620117872690','i18n-prefs':'USD','skin':'noskin','x-amz-captcha-1':'1653564743000398','x-amz-captcha-2':'uJUz242VbdtoL2dmvYELwA','session-token':'BqaLTgmOOlCVvvQIar47rE6fTI9z+3/mm+JG56xbC7zUperqJyUek2TX19ccLjiNFsESPzde8OjSMPEugnK/XtNky/CzmGA4WPmaMoSQ/C6DmCNmsw7+xrc5Zq8tcu2Y79xg3vVwowBtJSIimJDu+0iBT+QYsd1Fk60Ujl2A6RKBwTNdn3pUKpn5xVqbhQoG6GvbJTBHyROeAE7wu7uugg==	'}
    header=randHeader()
    url='https://www.amazon.com/dp/'+sku
    r = requests.get(url,headers=header,proxies=proxy_id,cookies=cookie)
    print(r.status_code,r.request.headers)
    return r.text

def get_data(sku_list):
    tim_r=np.random.randint(5,size=len(sku_list))
    ygsj = 0
    p = 0
    for i in tim_r:
        ygsj += i
    print('现在是' + time.strftime("%H:%M:%S", time.localtime()) + '\n预估总用时%d秒' % (ygsj))
    out_put_df = pd.DataFrame(
        columns=['日期', '时间', 'ASIN', '规格', '价格', '卖家', '发货', 'FBA库存数量', '排名', '类目', 'QA数', '评论数', '评分', '合并ASIN',
                 'ASIN上架时间'])
    out_put_sku = []
    for sku in sku_list:
        print('正常抓取第%d个产品' % (p + 1))
        try:
            res = get_res(sku)
        except Exception as err:
            p += 1
            print(sku, err)
            continue
        if 'APIs refer to our Marketplace APIs' in res:
            print('无效')
            break
        try:
            spec = re.findall('title-value a-text-bold">(.*?) <', res)[0]
        except:
            spec = ''
        try:
            rank = re.findall('</th> <td> <span>  <span>#(.*?) in ', res)[0]
        except:
            rank = ''
        try:
            calog = re.findall('<a href=.*?>(.*?)</a></span> <br/>', res)[0]
        except:
            calog = ''
        try:
            seller = re.findall("TriggerId'>(.*?)</a>", res)[0]
        except:
            seller = ''
        try:
            shipper = re.findall('<span class="a-size-small">(.*?)</span>', res)[0]
            if shipper == 'Amazon':
                shipper = 'FBA'
            else:
                shipper = 'FBM'
        except:
            shipper = ''

        try:
            stock = re.findall('> Only (.*?) left in stock - order soon. </span>', res)[0]
        except IndexError:
            try:
                stock = re.findall('a-size-base a-color-success a-text-bold"> (.*?) </span>', res)[0]
                stock = '>20'
            except IndexError:
                stock = '0'

        try:
            qa_count = re.findall(
                '<a id="askATFLink" class="a-link-normal askATFLink" href="#Ask"> <span class="a-size-base"> (.*?) answered questions </span> </a> </span>',
                res)[0]
        except:
            qa_count = 0

        try:
            rate_count = re.findall('acrCustomerReviewText" class="a-size-base">(.*?) ratings<', res)[1]
        except:
            rate_count = 0

        try:
            rate_star = re.findall('eviewCountTextLinkedHistogram noUnderline" title="(.*?) out of 5 stars">', res)[1]
        except:
            rate_star = 0

        try:
            spec_opt = re.findall('data-defaultAsin="(.*?)" data-dp-url=".*?" class="swatchAvailable">', res)

        except:
            spec_opt = ''
        try:
            up_data = \
            re.findall('Date First Available </th>  <td class="a-size-base prodDetAttrValue"> (.*?) </td> </tr>', res)[
                0]
        except:
            up_data = ''
        try:
            price = re.findall('a-offscreen">(.*?)<', res)[0]
        except:
            price = ''
        rq = time.strftime("%Y-%m-%d", time.localtime())
        sj = time.strftime("%H:%M:%S", time.localtime())
        t = time.time()

        out_put_df.loc[int(t)] = [rq, sj, sku, spec, price, seller, shipper, stock, rank, calog, qa_count, rate_count,
                                  rate_star, spec_opt, up_data]

        try:
            if spec_opt == '':
                pass
            else:
                for i in spec_opt:
                    out_put_sku.append(i)
        except:

            pass

        p += 1

        print('%s完成' % sku)
        time.sleep(10)

    return out_put_df, out_put_sku

while True:
    path_sku=os.path.join(os.getcwd()+'\\' + 'sku_list' + '.xlsx')
    path = os.path.join(os.getcwd()+'\\' + 'amz_info' + '.xlsx')

    if os.path.exists(path):
        print("file exist!")
        data=pd.read_excel(path)
    else:
        print("file not exist!")
        data=pd.DataFrame(columns=['日期','时间','ASIN','规格','价格','卖家','发货','FBA库存数量','排名','类目','QA数','评论数','评分','合并ASIN','ASIN上架时间'])

    if os.path.exists(path_sku):
        print("SKU file exist!")
        data_sku=pd.read_excel(path_sku)
    else:
        print("SKU file not exist!")
        data_sku=pd.DataFrame(['B09SV53Z57','B09KRJV89C','B09PNGKK6B','B09MRMX611'],columns=['sku'])
    sku_list=data_sku['sku'].to_list()

    ss=get_data(sku_list)

    out_put_data=ss[0]
    print(sku_list)
    for i in ss[1]:
        sku_list.append(i)
    sku_list=list(set(sku_list))

    data=pd.concat([data,out_put_data])
    data.to_excel(path,encoding='utf_8_sig',index=False)
    sku_df=pd.DataFrame(sku_list,columns=['sku'])
    sku_df.to_excel(path_sku,encoding='utf_8_sig',index=False)
    print('完成')
    for x in range(43200,-1,-1):
        mystr = "倒计时" + str(x) + "秒"
        print(mystr,end = "")
        print("\b" * (len(mystr)*2),end = "",flush=True)
        time.sleep(1)



