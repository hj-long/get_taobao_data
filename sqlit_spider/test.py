from sqlite3_model import GoodsInfo, GoodsDetail, SessionContext
import time

# # # 插入数据
# with SessionContext() as session:
#     for i in range(10):
#         good = GoodsInfo(name='test'+str(i), price='18')
#         detail = GoodsDetail(kuajing='test'+str(i), zhongliang='18')
#         good.detail.append(detail)
#         session.add(good)

# time.sleep(2)

# 查询数据
with SessionContext() as session:
    goods = session.query(GoodsDetail).all()
    for good in goods:
        print(good.kuajing, good.zhongliang)
        print('---------------')
        