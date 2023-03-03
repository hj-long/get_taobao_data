from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import time
from sqlite3_model import GoodsInfo, SessionContext


# 行星减速器
url = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%D0%D0%D0%C7%BC%F5%CB%D9%C6%F7&n=y&netType=1%2C11%2C16&spm=a260k.dacugeneral.search.0'
# 硬齿面减速机、行星减速机
# url1 = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%D0%D0%D0%C7%BC%F5%CB%D9%C6%F7&n=y&netType=1%2C11%2C16&spm=a260k.dacugeneral.search.0&beginPage=1&featurePair=1835%3A44231132%3B3310%3A23539333%3B9112%3A94585628'

url1 = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%D0%D0%D0%C7%BC%F5%CB%D9%C6%F7&spm=a26352.13672862.searchbox.input'

def driver_init():
    # 加载配置数据
    profile_dir = r'--user-data-dir=C:\Users\hjl\AppData\Local\Google\Chrome\User Data'
    c_option = webdriver.ChromeOptions()
    c_option.add_experimental_option('useAutomationExtension', False)
    c_option.add_experimental_option('excludeSwitches', ['enable-automation'])

    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            },
        'profile.password_manager_enabled': False,
        'credentials_enable_service': False
    }
    c_option.add_experimental_option('prefs', prefs)

    # 开发者模式防止被识别出
    # 网址：https://blog.csdn.net/dslkfajoaijfdoj/article/details/109146051
    c_option.add_experimental_option('excludeSwitches', ['enable-automation'])
    c_option.add_argument("--disable-blink-features=AutomationControlled")
    # c_option.add_experimental_option('w3c', False)

    c_option.add_argument(profile_dir)
    driver = webdriver.Chrome(chrome_options=c_option)
    # 执行cdp命令
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                  """
    })

    return driver

# 打开链接获取商品的详细信息
def get_goods_detail(driver, link):
    
    while True:
        try:
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
            # 定义商品详情表的数据字典
            data = []
            for span in goods_div:
                name = span.find_element(By.CLASS_NAME, 'offer-attr-item-name').text.strip()
                value = span.find_element(By.CLASS_NAME, 'offer-attr-item-value').text.strip()
                item = {
                    'name': name,
                    'value': value
                }
                data.append(item)

            print('商品信息获取完毕')
            # 关闭当前窗口
            driver.close()
            # 切换回原来的窗口
            driver.switch_to.window(original_window)
            # 返回商品详情表的数据字典
            return str(data)
        
        except:
            input('请手动滑动滑块，然后按回车键继续')
            continue


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
        print('-----------------')
        print(title, price, sale_sum)
        # 插入数据
        with SessionContext() as session:
            # 获取商品详细信息
            detail_data = get_goods_detail(driver, link)
            # 插入数据
            goods = GoodsInfo(title=title, price=price, sale_sum=sale_sum, link=link, detail=detail_data)
            session.add(goods)
            session.commit()

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