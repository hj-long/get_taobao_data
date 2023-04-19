from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
# 导入动作链模块
from selenium.webdriver import ActionChains
import time
import csv
import datetime

# 滑块验证
script = """
    Object.defineProperties(navigator, 'webdriver', {
        get: () => undefined
    })
"""


url = 'https://www.taobao.com/'

with open(f'./resource/goodsInfo_{datetime.date.today()}.csv', 'w', encoding='utf-8', newline='') as files:
    # 设置表头并写入csv文件
    csv_obj = csv.DictWriter(files, fieldnames=['商品名称', '商品详细分类', '商品分类价格'])
    csv_obj.writeheader()

    profile_dir = r'--user-data-dir=C:\Users\hjl\AppData\Local\Google\Chrome\User Data'
    # 加载配置数据
    c_option = webdriver.ChromeOptions()
    c_option.add_argument(profile_dir)
    # 实现规避检测
    c_option.add_argument('--disable-blink-features=AutomationControlled')
    # 启动浏览器并配置
    driver = webdriver.Chrome(chrome_options=c_option)

    # 滑块验证
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': script
    })

    driver.get(url)
    # 等待浏览器加载完毕
    driver.implicitly_wait(7)

    # 搜索商品
    search_keyWord = driver.find_element(By.ID, 'q').send_keys('行星减速器')
    search_btn = driver.find_element(By.CLASS_NAME, 'btn-search').click()
    # 存放原始窗口句柄
    original_window = driver.current_window_handle

    # 获取商品信息的列表
    goods_list = driver.find_elements(By.CLASS_NAME, 'ctx-box')

    for goods in goods_list:
        goods_title = goods.find_element(By.CLASS_NAME, 'J_ClickStat').text
        print(f'进入第{goods_list.index(goods) + 1}个商品具体分类')

        # 点击商品链接
        goods_link = goods.find_element(By.CLASS_NAME, 'J_ClickStat').click()
        # 切换到新的窗口
        driver.switch_to.window(driver.window_handles[-1])

        # 获取商品详情页的商品信息
        goods_box = driver.find_elements(By.CLASS_NAME, 'tb-txt') 
        name_list = []
        price_list = []

        try:
            # 判断是否有滑块验证
            if len(driver.find_elements(By.CLASS_NAME, 'nc-lang-cnt')) != 0:
                print('发现滑块验证')
                actionSpan()
                time.sleep(1)

            # 判断是否有商品分类
            if len(goods_box) == 0:
                box = driver.find_element(By.CLASS_NAME, 'J_TSaleProp')
                goods_box = box.find_elements(By.TAG_NAME, 'li')

            if len(goods_box) != 0:
                for g in goods_box:
                    name = g.find_element(By.TAG_NAME, 'span').text
                    g.click()
                    time.sleep(1)
                    price = driver.find_element(By.ID, 'J_StrPrice').text
                    name_list.append(name)
                    price_list.append(price)
        except Exception as e:
            print('发生错误：',e)
            
        dict = {
            '商品名称': goods_title,
            '商品详细分类': name_list,
            '商品分类价格': price_list
        }
        csv_obj.writerow(dict)
        driver.close()
        # 切换回原来的窗口
        print('切换回商品列表页')
        driver.switch_to.window(original_window)
    

    # 拖动滑块验证
    def actionSpan():
        span = driver.find_element(By.CLASS_NAME, 'nc-lang-cnt')
        # 实例化动作链对象
        action = ActionChains(driver)
        # 点击并按住滑块
        action.click_and_hold(span).perform()
        # 拖动滑块
        action.move_by_offset(300, 0).perform()
        # 释放鼠标
        action.release().perform()
        time.sleep(2)

    driver.quit()