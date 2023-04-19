from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import csv
import datetime

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


driver = driver_init()
driver.get(url1)
# 等待浏览器加载完毕
driver.implicitly_wait(7)
# 存放原始窗口句柄
original_window = driver.current_window_handle


# 打开链接获取商品信息
def open_link(link_a, driver):
    # 点击链接
    link_a.click()
    # 等待浏览器加载完毕
    driver.implicitly_wait(7)
    # 获取所有窗口句柄
    all_handles = driver.window_handles
    # 切换到新窗口
    for handle in all_handles:
        if handle != original_window:
            driver.switch_to.window(handle)
            break
    # 获取商品信息
    goods_div = driver.find_elements(By.XPATH, '//div[@class="offer-attr-list"]/div[@class="offer-attr-item"]')
    for span in goods_div:
        name = span.find_element(By.CLASS_NAME, 'offer-attr-item-name').text
        value = span.find_element(By.CLASS_NAME, 'offer-attr-item-value').text
        print(f'{name}：{value}')
    # 关闭当前窗口
    driver.close()
    # 切换回原来的窗口
    driver.switch_to.window(original_window)



with open(f'./resource/goodsInfo_{datetime.date.today()}.csv', 'w', encoding='utf-8', newline='') as files:
    # 设置表头并写入csv文件
    csv_obj = csv.DictWriter(files, fieldnames=['商品名称', '商品价格', '销量', '店铺链接'])
    csv_obj.writeheader()
    # 获取商品信息的列表
    goods_list =  driver.find_element(By.ID, 'sm-offer-list').find_elements(By.CLASS_NAME, 'space-offer-card-box')
    print('-----------------')
    print('开始爬取数据，数据长度为：', len(goods_list))
    for li in goods_list:
        link_div = li.find_element(By.CLASS_NAME, 'mojar-element-title').find_element(By.TAG_NAME, 'a')
        # 打开店铺获取商品信息
        open_link(link_div, driver)

        link = link_div.get_attribute('href')
        title = li.find_element(By.CLASS_NAME, 'mojar-element-title').find_element(By.CLASS_NAME, 'title').text
        price_div = li.find_element(By.CLASS_NAME, 'mojar-element-price')
        price = price_div.find_element(By.CLASS_NAME, 'showPricec').text
        sale_sum = price_div.find_element(By.CLASS_NAME, 'sale').text
        print(f'商品名称：{title}, 商品价格：{price}, 销量：{sale_sum}')
        # 写入csv文件
        csv_obj.writerow({'商品名称': title, '商品价格': price, '销量': sale_sum, '店铺链接': link})
    

print('-----------------')
print('爬取完毕！')
# 关闭浏览器
driver.quit()