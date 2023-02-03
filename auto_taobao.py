from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import csv
import datetime
import time

url = 'https://www.taobao.com/'

with open(f'./resource/taobao_{datetime.date.today()}.csv', 'w', encoding='utf-8', newline='') as files:
    # 设置表头并写入csv文件
    csv_obj = csv.DictWriter(files, fieldnames=['商品名称', '商品价格', '店铺名称', '店铺地址', '购买人数', '商品链接'])
    csv_obj.writeheader()

    profile_dir = r'--user-data-dir=C:\Users\hjl\AppData\Local\Google\Chrome\User Data'
    # 加载配置数据
    c_option = webdriver.ChromeOptions()
    c_option.add_argument(profile_dir)
    c_option.add_experimental_option('excludeSwitches', ['enable-loggin'])
    # 启动浏览器并配置
    driver = webdriver.Chrome(chrome_options=c_option)
    driver.get(url)
    # 等待浏览器加载完毕
    driver.implicitly_wait(7)


    search_keyWord = driver.find_element(By.ID, 'q').send_keys('行星减速器')
    search_btn = driver.find_element(By.CLASS_NAME, 'btn-search').click()

    def get_goodsInfo():
        # 获取商品信息的列表
        goods_list = driver.find_elements(By.CLASS_NAME, 'ctx-box')

        for goods in goods_list:
            goods_title = goods.find_element(By.CLASS_NAME, 'J_ClickStat').text
            goods_price = goods.find_element(By.CLASS_NAME, 'g_price-highlight').text
            goods_store = goods.find_element(By.CLASS_NAME, 'J_ShopInfo').text
            goods_location = goods.find_element(By.CLASS_NAME, 'location').text
            goods_people = goods.find_element(By.CLASS_NAME, 'deal-cnt').text
            goods_link = goods.find_element(By.CLASS_NAME, 'J_ClickStat').get_attribute('href')
            dict_goods = {
                '商品名称': goods_title, 
                '商品价格': goods_price, 
                '店铺名称': goods_store, 
                '店铺地址': goods_location, 
                '购买人数': goods_people, 
                '商品链接': goods_link
                }
            csv_obj.writerow(dict_goods)

    for page in range(1, 11):
        time.sleep(2)
        get_goodsInfo()
        print(f'第{page}页数据已经写入csv文件')
        driver.find_element(By.CLASS_NAME, 'icon-btn-next-2').click()
    
    driver.quit()