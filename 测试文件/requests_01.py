import requests
import re
import csv
import time


url = 'https://movie.douban.com/top250'
def getWebData(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"
    }
    # 添加设备的头信息后，数据获取成功了
    response = requests.get(url=url, headers=header)
    # 使用re模块的正则表达式进行目标内容的提取
    obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)'
                    r'</span>.*?<p class="">.*?<br>(?P<year>.*?)&nbsp;.*?'
                    r'<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
                    r'<span>(?P<num>.*?)人评价</span>'
        , re.S)
    # 开始匹配
    result = obj.finditer(response.text)
    file = open('./resource/movie_data.csv', 'a+', encoding='utf-8')
    csv_data = csv.writer(file)
    for it in result:
        # print(it.group("name"))
        # print(it.group("year").strip())
        # print(it.group("score"))
        # print(it.group("num"))
        dic = it.groupdict()
        dic["year"] = dic["year"].strip()
        csv_data.writerow(dic.values())
    file.close()
    return ''

for i in range(10):
    url1 = url + '?start='+ str(i*25) + '&filter='
    time.sleep(0.5)
    getWebData(url1)
print('处理完毕')





# with open('./movie250.html', 'w', encoding='utf-8') as f:
#     f.write(response.text)
# print('over')