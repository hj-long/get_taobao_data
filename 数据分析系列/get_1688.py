from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions,ActionChains
import time
from sqlite3_model import GoodsInfo, SessionContext, GoodsDetail
import re

# JZQ 系列减速器
# url = 'https://s.1688.com/selloffer/imall_search.htm?keywords=JZQ+%D4%B2%D6%F9%B3%DD%C2%D6%BC%F5%CB%D9%BB%FA&spm=a26352.22885112.searchbox.input'
# 158条，断了重新爬取
# url1 = 'https://s.1688.com/selloffer/imall_search.htm?keywords=JZQ+%D4%B2%D6%F9%B3%DD%C2%D6%BC%F5%CB%D9%BB%FA&spm=a26352.22885112.searchbox.input&beginPage=4#sm-filtbar'
# 279条，断了重新爬取
# url1 = 'https://s.1688.com/selloffer/imall_search.htm?keywords=JZQ+%D4%B2%D6%F9%B3%DD%C2%D6%BC%F5%CB%D9%BB%FA&spm=a26352.22885112.searchbox.input&beginPage=7#sm-filtbar'
# 329条，又jiba断了，重新爬取， 352条重新回7页爬到399条
# url1 = 'https://s.1688.com/selloffer/imall_search.htm?keywords=JZQ+%D4%B2%D6%F9%B3%DD%C2%D6%BC%F5%CB%D9%BB%FA&spm=a26352.22885112.searchbox.input&beginPage=8#sm-filtbar'

# NGW 系列减速器(记得改商品信息过滤判断条件为NGW),674断了，重新爬取
url1 = 'https://s.1688.com/selloffer/imall_search.htm?keywords=NGW&spm=&featurePair=1835%3A44231132&beginPage=7#sm-filtbar'


# 初始化浏览器
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

def get_goods_info(driver):
    # 获取商品信息的列表
    goods_list =  driver.find_element(By.ID, 'sm-offer-list').find_elements(By.CLASS_NAME, 'space-offer-card-box')
    print('-----------------')
    print('开始爬取数据，数据长度为：', len(goods_list))
    for li in goods_list:
        link_div = li.find_element(By.CLASS_NAME, 'mojar-element-title').find_element(By.TAG_NAME, 'a')
        link = link_div.get_attribute('href')
        title = li.find_element(By.CLASS_NAME, 'mojar-element-title').find_element(By.CLASS_NAME, 'title').text

        # 过滤掉不是JZQ系列的商品
        # if 'ZQ' not in title:
        #     continue

        # 过滤掉不是NGW系列的商品
        if 'NGW' not in title:
            continue

        try:
            # 这个地方容易报错，所以用try，不知道为什么，有毒
            price_div = li.find_element(By.CLASS_NAME, 'mojar-element-price')
            price = price_div.find_element(By.CLASS_NAME, 'showPricec').text
            sale_sum = price_div.find_element(By.CLASS_NAME, 'sale').text
            if sale_sum == '':
                sale_sum = '0'
        except:
            continue
        print('-----------------')
        print(title, price, sale_sum)
        # 插入数据
        with SessionContext() as session:
            # 获取商品详细信息
            detail_data, address, factory_name = get_goods_detail(driver, link)
            # 插入商品信息
            goods = GoodsInfo(title=title, price=price, sale_sum=sale_sum, link=link, detail=detail_data, address=address, factory_name=factory_name)
            session.add(goods)
            session.commit()

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
            # 获取地址信息
            address_div = driver.find_element(By.XPATH, '//div[@id="shop-container-footer"]//div[@style="text-align: center;"]/p')
            # 获取厂家名称
            factory_name = address_div.find_elements(By.TAG_NAME, 'span')[0].text
            address = address_div.find_elements(By.TAG_NAME, 'span')[1].text.replace('地址：', '')
            print(factory_name, address)
            
            print('-----------------')
            # 定义商品详情表的数据字典
            data = []
            for span in goods_div:
                name = span.find_element(By.CLASS_NAME, 'offer-attr-item-name').text.strip()
                value = span.find_element(By.CLASS_NAME, 'offer-attr-item-value').text.strip()
                # 如果是 输入转速、输出转速、额定功率、许用扭矩，需要转换为数字
                if name in ['输入转速', '输出转速范围', '额定功率', '许用扭矩']:
                    value = handle_value(value)
                if name == '级数':
                    # 如果能转换为数字，说明是数字，否则是文字
                    try:
                        float(value)
                    except:
                        # 如果是 多级，转为2，单级转为1
                        if '多' in value:
                            value = '2'
                        elif '单' in value or '一' in value or '1' in value:
                            value = '1'
                        elif '二' in value or '2' in value or '两' in value or '双' in value:
                            value = '2'
                        elif '三' in value or '3' in value:
                            value = '3'
                        elif '四' in value or '4' in value:
                            value = '4'
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
            return (str(data), address, factory_name)
        
        except:
            # 手动处理滑动验证
            input('请手动滑动验证码，输入任意字符继续：')
            continue

# 处理字段值中存在的特殊字符、单位、空格、范围值等
def handle_value(value):
    # 去除空格
    value = value.replace(' ', '')
    # 出现中文的 （）, 也可能出现英文的(),可能有多个括号，用正则表达式一起去掉
    value = re.sub(r'（.*?）', '', value)
    value = re.sub(r'\(.*?\)', '', value)
    # 去除单位 rpm、kw、Nm, 忽略大小写
    value = value.replace('rpm', '')
    value = value.replace('Kw', '')
    value = value.replace('KW', '')
    value = value.replace('kw', '')
    value = value.replace('kW', '')
    value = value.replace('k.W', '')
    value = value.replace('k.w', '')
    value = value.replace('K.W', '')
    value = value.replace('K.w', '')
    value = value.replace('N.m', '')
    value = value.replace('N.M', '')
    value = value.replace('n.m', '')
    value = value.replace('n.M', '')
    value = value.replace('Nm', '')
    value = value.replace('nm', '')
    value = value.replace('NM', '')
    value = value.replace('nM', '')

    # 如果全是中文或者全是英文，直接返回 0
    if re.match(r'^[\u4e00-\u9fa5]+$', value):
        return 0
    if re.match(r'^[a-zA-Z]+$', value):
        return 0
    # 如果有中文，需要去掉中文
    if re.search(r'[\u4e00-\u9fa5]+', value):
        value = re.sub(r'[\u4e00-\u9fa5]+', '', value)
        # 如果有/，先判断是不是两个数字，如果不是，取第一个数字
        if '/' in value:
            arr = value.split('/')
            value = value_arr(arr)

    # 如果有多组数据，例如有, ， 、两个 / 以上，取第一个数字或者第二个数字
    if ',' in value:
        arr = value.split(',')
        value = value_arr(arr)
    if '，' in value:
        arr = value.split('，')
        value = value_arr(arr)
    if '、' in value:
        arr = value.split('、')
        value = value_arr(arr)
    if '/' in value:
        arr = value.split('/')
        value = value_arr(arr)
    
    return value

# 判断数字数组取值
def value_arr(arr):
    value = 0
    if len(arr) >= 2 and arr[0].isdigit() and arr[1].isdigit():
        # 如果第一个数字比1小，取第二个数字
        if float(arr[0]) <= 1:
            value = arr[1]
        else:
            value = arr[0]
    else:
        value = arr[0]
    return value

# 程序入口
if __name__ == '__main__':
    driver = driver_init()
    driver.implicitly_wait(3)  
    # 打开链接获取商品信息
    driver.get(url1)
    # 睡眠1秒，等待浏览器加载完毕
    time.sleep(2)
    # 循环爬取40页数据
    for i in range(40):
        print(f'-----------------第{i+1}页-----------------')
        # 等待浏览器加载完毕
        driver.implicitly_wait(7)
        # 获取当前窗口句柄
        original_window = driver.current_window_handle
        # 获取下一页的按钮
        next_btn = driver.find_element(By.CLASS_NAME, 'fui-next')
        time.sleep(1)
        # 慢慢向下滚动
        for i in range(1, 3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        # 再慢慢向上滚动
        for i in range(1, 3):
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
        # 滑动鼠标到页面中部
        ActionChains(driver).move_by_offset(0, 300).perform()
        time.sleep(1)

        # 获取商品信息
        get_goods_info(driver)
        # 点击下一页
        try:
           next_btn.click()
        except:
            break