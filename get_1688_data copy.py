from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import time
import sqlite3

# 创建数据库
conn = sqlite3.connect(f'spider_1688.db')
# 创建游标
cursor = conn.cursor()
# 创建表,一个是商品信息表(商品名称，价格，销量)，一个是商品具体的详细信息表(都非必填)，两个表之间通过商品ID进行关联
cursor.execute('create table goods_info \
    (id integer primary key autoincrement, name varchar(100), company varchar(100)\
        price varchar(100), sales varchar(100), shop_link varchar(100))')

cursor.execute('create table goods_detail \
    (id integer primary key autoincrement,\
            kuajing varchar(100), \
            zhongliang varchar(100), dinghuo varchar(100)), jiagong varchar(100), \
            num varchar(100), leibie varchar(100), chilunleibie varchar(100), \
            anzhuang varchar(100), buju varchar(100), chilunyingdu varchar(100), \
            yongtu varchar(100), pinpai varchar(100), xinghao varchar(100), \
            shuru varchar(100), shuchu varchar(100), endinggonglv varchar(100), \
            niuju varchar(100), fanwei varchar(100), jishu varchar(100), \
            guige varchar(100), chukou varchar(100), jiansubi varchar(100), \
            chuangdongbi varchar(100), ADD FOREIGN KEY (id) REFERENCES goods_info(id))')
conn.commit()

# 建立表哈希表，用于存储商品信息
detail_name = dict()
name_map = ["跨境", "单位重量", "订货号", "加工定制", "货号", "类别", "齿轮类型", "安装形式",
            "布局形式", "齿面硬度", "用途", "品牌", "型号", "输入转速", "输出转速范围",
            "额定功率", "许用扭矩", "使用范围", "级数", "规格", "是否跨境出口专供货源", "减速比","传动比"
            ]
value_map = ["kuajing", "zhongliang", "dinghuo", "jiagong", "num", "leibie", "chilunleibie","anzhuang", 
            "buju", "chilunyingdu", "yongtu", "pinpai", "xinghao", "shuru", "shuchu",
            "endinggonglv", "niuju", "fanwei", "jishu", "guige", "chukou", "jiansubi", "chuangdongbi"
            ]

for i in range(len(name_map)):
    detail_name[name_map[i]] = value_map[i]


# 行星减速器
url = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%D0%D0%D0%C7%BC%F5%CB%D9%C6%F7&n=y&netType=1%2C11%2C16&spm=a260k.dacugeneral.search.0'
# 硬齿面减速机、行星减速机
url1 = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%D0%D0%D0%C7%BC%F5%CB%D9%C6%F7&n=y&netType=1%2C11%2C16&spm=a260k.dacugeneral.search.0&beginPage=1&featurePair=1835%3A44231132%3B3310%3A23539333%3B9112%3A94585628'

def driver_init():
    # 加载配置数据
    profile_dir = r'--user-data-dir=C:\Users\hjl\AppData\Local\Google\Chrome\User Data'
    c_option = webdriver.ChromeOptions()
    c_option.add_argument(profile_dir)
    c_option.add_argument('--ignore-certificate-errors-spki-list')
    c_option.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(chrome_options=c_option)
    return driver

# 打开链接获取商品的详细信息
def get_goods_detail(driver, link):
    # 打开新窗口
    driver.execute_script("window.open('"+link+"')")
    # 等待浏览器加载完毕
    driver.implicitly_wait(7)
    # 获取所有窗口句柄
    all_handles = driver.window_handles
    # 切换到新窗口
    for handle in all_handles:
        if handle != original_window:
            driver.switch_to.window(handle)
            break
    time.sleep(2)
    # 先点击展开按钮
    try:
        driver.find_element(By.CLASS_NAME, 'offer-attr-switch').click()
    except:
        pass
    time.sleep(1)
    # 获取商品信息
    goods_div = driver.find_elements(By.XPATH, '//div[@class="offer-attr-list"]/div[@class="offer-attr-item"]')
    print('-----------------')
    for span in goods_div:
        name = span.find_element(By.CLASS_NAME, 'offer-attr-item-name').text
        value = span.find_element(By.CLASS_NAME, 'offer-attr-item-value').text
        # 判断是否是需要的数据
        if name in detail_name:
            name = detail_name[name]
            # 插入数据库
            cursor.execute('insert into goods_detail (%s) values ("%s")' % (name, value))
            conn.commit()
    print('商品信息获取完毕')
    # 关闭当前窗口
    driver.close()
    # 切换回原来的窗口
    driver.switch_to.window(original_window)


def get_goods_info(driver):
    # 获取商品信息的列表
    goods_list =  driver.find_element(By.ID, 'sm-offer-list').find_elements(By.CLASS_NAME, 'space-offer-card-box')
    print('-----------------')
    print('开始爬取数据，数据长度为：', len(goods_list))
    for li in goods_list:
        link_div = li.find_element(By.CLASS_NAME, 'mojar-element-title').find_element(By.TAG_NAME, 'a')
        link = link_div.get_attribute('href')
        title = li.find_element(By.CLASS_NAME, 'mojar-element-title').find_element(By.CLASS_NAME, 'title').text
        price_div = li.find_element(By.CLASS_NAME, 'mojar-element-price')
        price = price_div.find_element(By.CLASS_NAME, 'showPricec').text
        sale_sum = price_div.find_element(By.CLASS_NAME, 'sale').text
        if sale_sum == '':
            sale_sum = '0'
        # 调用获取商品详细信息的方法
        get_goods_detail(driver, link)
        # 插入数据
        cursor.execute(f'insert into goods_info (name, price, sales, link) values ("{title}", "{price}", "{sale_sum}", "{link}")')
        conn.commit()

# 程序入口
if __name__ == '__main__':
    driver = driver_init()
    driver.implicitly_wait(3)
    # 打开链接获取商品信息
    driver.get(url)
    # 睡眠3秒，等待浏览器加载完毕
    time.sleep(3)
    # 获取当前窗口句柄
    original_window = driver.current_window_handle
    # 慢慢向下滚动
    for i in range(1, 10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    # 获取商品信息
    get_goods_info(driver) 


print('-----------------')
print('爬取完毕！')
# 关闭浏览器
driver.quit()