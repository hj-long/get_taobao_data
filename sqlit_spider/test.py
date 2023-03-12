from sqlite3_model import GoodsInfo, SessionContext
import time

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