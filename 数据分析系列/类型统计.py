from sqlite3_model import GoodsInfo, SessionContext, GoodsDetail
import re

# 从GoodsDetail取出所有的数据
with SessionContext() as session:
    data = session.query(GoodsDetail).all()
    # 循环取出每条数据的detail字段
    for item in data:
        # 检查 orders_goods、type、type_num 类型是否正确

        if item.orders_goods is not None:
            # 正则表达式判断如果item.orders_goods是纯数字、纯中文，则设置为None
            val1 = item.orders_goods
            if re.match(r'^\d+$', item.orders_goods) or re.match(r'^[\u4e00-\u9fa5]+$', item.orders_goods):
                item.orders_goods = None
            # 如果item.orders_goods是类似 JZQ500圆柱齿轮减速器，需要将JZQ500提取出来
            elif re.match(r'^[A-Za-z]+', item.orders_goods):
                item.orders_goods = re.match(r'^[A-Za-z]+', item.orders_goods).group()
                
            # 查看前后变化
            print(item.id, val1, item.orders_goods)

        # 保存到数据库
        session.add(item)
    print('ok')
