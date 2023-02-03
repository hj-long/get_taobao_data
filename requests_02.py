import requests
import time
import re
import json
import csv
import random

with open('./resource/taobao_data_2.csv', 'w', encoding='utf-8', newline='') as files:
    # 设置表头标题，写入数据
    csv_obj = csv.DictWriter(files, fieldnames=['标题', '价格', '店铺', '购买人数', '地点', '商品详情页', '店铺链接', '图片链接'])
    csv_obj.writeheader()
    for page in range(0, 26):
        print(f'----------------正在爬取第{page}页-------------------------')
        urls = f'https://s.taobao.com/search?q=%E8%A1%8C%E6%98%9F%E5%87%8F%E9%80%9F%E5%99%A8&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20230114&ie=utf8&bcoffset=1&ntoffset=1&p4ppushleft=2%2C48&s={ page * 44}'
        time.sleep(random.randint(1, 5))
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "Cookie":"_m_h5_tk=d08c7eaaf12f82c007f23655c0f22f9d_1673700102315; _m_h5_tk_enc=64e73cb06b641057cfaa77eaeded4343; cna=321JHIRqYxEBASQJilUj+nux; xlly_s=1; t=3222501e3802531a7a7f175f2cfc2898; _samesite_flag_=true; cookie2=119b9f5b76a0946a0bfb05b8141fe216; _tb_token_=53e715e7753be; sgcookie=E100F0BMT58BFWcEW9iozuwcXMb2S9UANdGZ1BtyRomRDScXyswpOwb%2BKD7chUZUUU4LX3Ih%2FyS%2FKdDit1WaQLVFvgSOl84YKbgfzop4Xgb9JF8%3D; unb=2528679550; uc1=existShop=false&pas=0&cookie14=UoezTG8mglwzTQ%3D%3D&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie15=V32FPkk%2Fw0dUvg%3D%3D&cookie21=URm48syIYB3rzvI4Dim4; uc3=nk2=05SrVV98BFtwfA%3D%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D&vt3=F8dCvjMtwpsebFrd2UM%3D&id2=UU2w5i%2BWehFvzg%3D%3D; csg=45fbb00e; lgc=%5Cu9738%5Cu6C14%5Cu7684%5Cu9F99%5Cu53D4; cancelledSubSites=empty; cookie17=UU2w5i%2BWehFvzg%3D%3D; dnk=%5Cu9738%5Cu6C14%5Cu7684%5Cu9F99%5Cu53D4; skt=33e3c92cc9219873; existShop=MTY3MzY5MTIxMw%3D%3D; uc4=id4=0%40U2%2F301n2q%2Fn1XZ2bupir7YOUP8iD&nk4=0%400S%2FTDglR3XLlerFViO4SPEOhHwgN; tracknick=%5Cu9738%5Cu6C14%5Cu7684%5Cu9F99%5Cu53D4; _cc_=W5iHLLyFfA%3D%3D; _l_g_=Ug%3D%3D; sg=%E5%8F%9408; _nk_=%5Cu9738%5Cu6C14%5Cu7684%5Cu9F99%5Cu53D4; cookie1=B0BQ1OA8SD%2B4rdjFt6hT2qckqW8ReDEHniyKqWK4Piw%3D; JSESSIONID=EEEF1C6E6236F5DF3812B8DD32389CCC; isg=BH5-hYe1keuGKsXPJy3-1Sy6z5TAv0I549DCkiiH6kG8yx6lkE-SSaSpR5cHaDpR; l=fBTVJNY7TZBpgcQyBOfaFurza77OSIRYYuPzaNbMi9fPOv5B5Q8GW6R4M8L6C3GVF6WvR3PZC7jvBeYBqQAonxv92j-la_kmndLHR35..; tfstk=cGv1BRg2OP46LwH0INiEb9LlOpBAwHgCxf_9fVLnkexPEa1mx87WEXd0-tSAA",
            "Pragma":"no-cache",
            "Referer":"https://s.taobao.com/search/_____tmd_____/page/login_jump?rand=S3WxGHAgAt756EpznwfNzJq2AFA2qBNla3j6EINUS8We9dazM_iKElp8DwVSHZUevpC41Bx7RzivXIj9RnZgdg&_lgt_=ae1c526f29d96a1b3171920fd67badc7___215918___bcca30b46146905d76ffab61f57da2c2___837b211a0c5c4d0311617da5fff37e25001413704de625b860e2518faad0f0365954186819fa3d51c24403c5c40646b9c2b567bee5ae745babdbe22710bac8810c7d02c1d51d1ee1460adbd0cb04d030f0e031931b9132ad85013eb3be5f87fdfda1ffe6d0052b26010cff24765b937333be60e83f16310c86c494a16dd5d1b16c7f2de620667f2e22d717e3d5c8f4f1ef8b8415db5cc8cb7b25c3032c6b30b5&x5referer=https://s.taobao.com/search?q=%E8%A1%8C%E6%98%9F%E5%87%8F%E9%80%9F%E5%99%A8&suggest=history_1&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.jianhua.201856-taobao-item.2&ie=utf8&initiative_id=tbindexz_20170306&_input_charset=utf-8&wq=&suggest_query=&source=suggest",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }
        response = requests.get(url=urls, headers=headers)
        html_data = re.findall(r'g_page_config = (.*?)}};', response.text)[0]
        html_data += '}}'
        # 转成json格式的数据，提取关键信息
        json_data = json.loads(html_data)
        res_data = json_data['mods']['itemlist']['data']['auctions']
        for index in res_data:
            dict = {
                "标题": index['raw_title'],
                "价格": index['view_price'],
                "店铺": index['nick'],
                "购买人数": index['view_sales'],
                "地点": index['item_loc'],
                "商品详情页": index['detail_url'],
                "店铺链接": index['shopLink'],
                "图片链接": index['pic_url']
            }
            csv_obj.writerow(dict)
        response.close()

    print('over!')
