from sqlite3_model import GoodsInfo, SessionContext, GoodsDetail
import re


# 统计函数
def type_count(item, flag):
    # 统计ZQ系列类别函数
    type_item1 = ['ZQ175', 'ZQ200', 'ZQ250', 'ZQ350', 'ZQ400', 'ZQ500', 'ZQ650', 'ZQ750', 'ZQ850', 'ZQ1000']
    # 统计NGW系列类别函数
    type_item2 = ['NGW21', 'NGW31', 'NGW41','NGW42','NGW51','NGW52','NGW61','NGW62','NGW63','NGW71','NGW72','NGW73','NGW81','NGW82','NGW83','NGW91','NGW92','NGW93',
                    'NGW101','NGW102','NGW103','NGW111','NGW112','NGW113','NGW114','NGW121','NGW122','NGW123','NGW132','NGW160','NGW180','NGW200','NGW225','NGW250' 
                  ]
    if flag == 1:
        type_item = type_item1
    else:
        type_item = type_item2
    for type in type_item:
        # 忽略大小写
        if type.lower() in item.lower():
            if flag == 1:
                return 'J' + type
            return type
    return 'other'


# 从GoodsDetail取出399-819条数据
with SessionContext() as session:
    data = session.query(GoodsDetail).filter(GoodsDetail.id >= 399, GoodsDetail.id <= 819).all()
    # 统计类别(jzq100跟jzq1000重复了，手动统计)
    # type_item = {
    #         'JZQ100': 1,
    #         'JZQ175': 0,
    #         'JZQ200': 0,
    #         'JZQ250': 0,
    #         'JZQ350': 0,
    #         'JZQ400': 0,
    #         'JZQ500': 0,
    #         'JZQ650': 0,
    #         'JZQ750': 0,
    #         'JZQ850': 0,
    #         'JZQ1000': 0,
    #         'other': 0,
    #         'None': 0
    #     } 

    # 统计类别
    type_item = {
            'NGW11': 2,
            'NGW21': 0,
            'NGW31': 0,
            'NGW41': 0,
            'NGW42': 0,
            'NGW51': 0,
            'NGW52': 0,
            'NGW61': 0,
            'NGW62': 0,
            'NGW63': 0,
            'NGW71': 0,
            'NGW72': 0,
            'NGW73': 0,
            'NGW81': 0,
            'NGW82': 0,
            'NGW83': 0,
            'NGW91': 0,
            'NGW92': 0,
            'NGW93': 0,
            'NGW101': 0,
            'NGW102': 0,
            'NGW103': 0,
            'NGW111': 0,
            'NGW112': 0,
            'NGW113': 0,
            'NGW114': 0,
            'NGW121': 0,
            'NGW122': 0,
            'NGW123': 0,
            'NGW132': 0,
            'NGW160': 0,
            'NGW180': 0,
            'NGW200': 0,
            'NGW225': 0,
            'NGW250': 0,
            'other': 0,
            'None': 0
        }

    for item in data:
        if item.type_num is not None:
            # type_item[type_count(item.type_num, 1)] += 1
            type_item[type_count(item.type_num, 2)] += 1
        elif item.orders_goods is not None:
            # type_item[type_count(item.orders_goods, 1)] += 1
            type_item[type_count(item.orders_goods, 2)] += 1
        elif item.num is not None:
            # type_item[type_count(item.num, 1)] += 1
            type_item[type_count(item.num, 2)] += 1
        else:
            type_item['None'] += 1

    print(type_item)
    print('ok')




























#------------------------------------------------------------
        # if item.type_num is not None:
        #     # 正则表达式判断如果item.orders_goods是纯数字、纯中文，则设置为None
        #     val1 = item.type_num
        #     if re.match(r'^\d+$', item.type_num) or re.match(r'^[\u4e00-\u9fa5]+$', item.type_num):
        #         print(val1, '被清空')
        #         item.type_num = None
#------------------------------------------------------------
        # if item.orders_goods is not None:
        #     val1 = item.orders_goods
        #     # 把type_num中的中文去掉
        #     item.orders_goods = re.sub(r'[\u4e00-\u9fa5]+', '', val1)
        #     print(val1, '=>', item.orders_goods)
#------------------------------------------------------------