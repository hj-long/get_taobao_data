from sqlite3_model import GoodsInfo, SessionContext, GoodsDetail
import re

# 从GoodsInfo表中取出所有数据
def make_data():
    with SessionContext() as session:
        data = session.query(GoodsInfo).all()
        name_list = {
                '跨境包裹重量': 'cross_bag_weight', '单位重量': 'unit_weight', '订货号': 'orders_goods',
                '加工定制': 'process','货号': 'num', '类别': 'type', '齿轮类型': 'wheel_type', '安装形式': 'installation',
                '布局形式': 'layout', '齿面硬度': 'wheel_hard', '用途': 'usage', '品牌': 'brand', '型号': 'type_num',
                '输入转速': 'input_rev', '输出转速范围': 'output_rev', '额定功率': 'rating_power', '许用扭矩': 'allowable_torque', '使用范围': 'use_scope',
                '额定电压': 'rating_V', '额定电流': 'rating_A', '额定转速': 'rating_speed', '额定转矩': 'rating_torque', '级数': 'series',
                '减速比': 'slow_ratio', '规格': 'size', '主要销售地区': 'sales_area', '有可授权的自有品牌': 'is_brand', '是否跨境出口专供货源': 'is_cross',
            }
        # 循环取出每条数据的detail字段
        for item in data:
            detail_data = eval(item.detail)
            # 循环取出每条数据的detail字段中的每个字典
            # 准备将数据插入到GoodsDetail表中
            good_detail = GoodsDetail()

            for i in detail_data:
                if name_list.get(i['name']) is not None:
                    # print(name_list[i['name']], i['name'], i['value'])
                    # 如果是输出转速范围，需要处理一下单位和特殊字符
                    if i['name'] == '输出转速范围':
                        value = i['value']
                        try:
                            float(i['value'])
                        except:
                            value = handle_value(i['value'])
                        setattr(good_detail, name_list[i['name']], value)
                    else:
                        setattr(good_detail, name_list[i['name']], i['value'])
            # 将GoodsDetail表中的id赋值给GoodsInfo表中的detail_id
            item.detail_id = good_detail.id
            # 将数据插入到GoodsDetail表中
            session.add(good_detail)
            print(item.detail_id)
        print('ok')


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

if __name__ == '__main__':
    make_data()