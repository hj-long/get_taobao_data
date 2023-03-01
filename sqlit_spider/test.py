from sqlite3_model import GoodsInfo, GoodsDetail, SessionContext
import time

# # 插入数据
# with SessionContext() as session:
#     for i in range(10):
#         good = GoodsInfo(title='test'+str(i), price='18')
#         detail = GoodsDetail(dinghuo='caonima'+str(i), jiagong='18')
#         session.add(good)
#         session.add(detail)

# time.sleep(2)

# 查询数据(修改数据)
with SessionContext() as session:
    goods = session.query(GoodsDetail).filter(GoodsDetail.id>5).all()
    for good in goods:
        print(good.dinghuo, good.jiagong)
        print('------------------')
        session.query(GoodsInfo).filter(GoodsInfo.id==good.id).update({'title':good.dinghuo})
        