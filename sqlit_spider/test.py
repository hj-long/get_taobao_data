from sqlite3_model import GoodsInfo, SessionContext, GoodsDetail
import time

# 从GoodsInfo表中取出所有数据
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
                # print(name_list[i['name']], i['value'])
                setattr(good_detail, name_list[i['name']], i['value'])
        # 将GoodsDetail表中的id赋值给GoodsInfo表中的detail_id
        item.detail_id = good_detail.id
        # 将数据插入到GoodsDetail表中
        session.add(good_detail)
        print(item.detail_id)
    print('ok')




















# # 插入数据
# with SessionContext() as session:
#     data = []
#     for i in range(10):
#         item = {
#             'name': f'name{i}',
#             'value': f'value{i}'
#         }
#         data.append(item)
#     data = str(data)
#     session.add(GoodsInfo(detail=data, title=f'title{i}', price='price', sale_sum='sale_sum', link='link'))

# time.sleep(2)

# # 查询数据(修改数据)
# with SessionContext() as session: 
#     # 查询数据
#     detail = session.query(GoodsInfo).filter(GoodsInfo.id == 1).first().detail
#     print(detail)
#     print(type(detail))
#     # 转换为list
#     d1 = eval(detail)
#     print(d1[0], d1[1].get('name'))
#     print(type(d1))

# data = {
#     "kuajing": "跨境包裹重量",
#     "zhongliang": "单位重量",
#     "dinghuo": "订货号",
#     "jiagong": "加工定制",
#     "num": "货号",
#     "leibie": "类别",
#     "chilunleibie": "齿轮类型",
#     "anzhuang": "安装形式",
#     "buju": "布局形式",
#     "chilunyingdu": "齿面硬度",
#     "yongtu": "用途",
#     "pinpai": "品牌",
#     "xinghao": "型号",
#     "shuru": "输入转速",
#     "endinggonglv": "额定功率",
#     "shuchu": "输出转速范围",
#     "niuju": "许用扭矩",
#     "fanwei": "使用范围",
#     "jishu": "级数",
#     "guige": "规格",
#     "chukou": "是否跨境出口专供货源",
#     "jiansubi": "减速比",
#     "chuangdongbi": "传动比"
# }