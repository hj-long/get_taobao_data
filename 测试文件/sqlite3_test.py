import sqlite3
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
# from sqlalchemy.orm import sessionmaker, relationship

# # 创建数据库连接
# engine = create_engine('sqlite:///spider_1688.db', echo=True)
# # 创建基类
# Base = declarative_base()

# # 创建商品信息表
# class GoodsInfo(Base):
#     __tablename__ = 'goods_info'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100))
#     company = Column(String(100))
#     price = Column(String(100))
#     sales = Column(String(100))
#     shop_link = Column(String(100))

# # 创建商品详细信息表(非必填项)
# class GoodsDetail(Base):
#     __tablename__ = 'goods_detail'
#     id = Column(Integer, primary_key=True)
#     kuajing = Column(String(100))
#     zhongliang = Column(String(100))
#     dinghuo = Column(String(100))
#     jiagong = Column(String(100))
#     num = Column(String(100))
#     leibie = Column(String(100))
#     chilunleibie = Column(String(100))
#     anzhuang = Column(String(100))
#     buju = Column(String(100))
#     chilunyingdu = Column(String(100))
#     yongtu = Column(String(100))
#     pinpai = Column(String(100))
#     xinghao = Column(String(100))
#     shuru = Column(String(100))
#     shuchu = Column(String(100))
#     endinggonglv = Column(String(100))
#     niuju = Column(String(100))
#     fanwei = Column(String(100))
#     jishu = Column(String(100))
#     guige = Column(String(100))
#     chukou = Column(String(100))
#     jiansubi = Column(String(100))
#     chuangdongbi = Column(String(100))
#     goods_id = Column(Integer, ForeignKey('goods_info.id'))

# # 测试类
# class Test(Base):
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100))
#     age = Column(Integer)
# metadata = Base.metadata

# # 创建数据库表
# Base.metadata.create_all(engine)

# # 创建会话
# Session = sessionmaker(bind=engine)


# # 插入数据
# session = Session()
# for i in range(10):
#     test = Test(name='test', age=18)
#     session.add(test)

# # 提交数据
# session.commit()



## **********************************************

# # 创建数据库
# conn = sqlite3.connect(f'spider_1688.db')
# # 创建游标
# cursor = conn.cursor()
# # 创建表,一个是商品信息表(商品名称，价格，销量)，一个是商品具体的详细信息表(都非必填)，两个表之间通过商品ID进行关联
# cursor.execute('create table goods_info \
#     (id integer primary key autoincrement, name varchar(100), company varchar(100)\
#         price varchar(100), sales varchar(100), shop_link varchar(100))')

# cursor.execute('create table goods_detail \
#     (id integer primary key autoincrement,\
#             kuajing varchar(100), \
#             zhongliang varchar(100), dinghuo varchar(100)), jiagong varchar(100), \
#             num varchar(100), leibie varchar(100), chilunleibie varchar(100), \
#             anzhuang varchar(100), buju varchar(100), chilunyingdu varchar(100), \
#             yongtu varchar(100), pinpai varchar(100), xinghao varchar(100), \
#             shuru varchar(100), shuchu varchar(100), endinggonglv varchar(100), \
#             niuju varchar(100), fanwei varchar(100), jishu varchar(100), \
#             guige varchar(100), chukou varchar(100), jiansubi varchar(100), \
#             chuangdongbi varchar(100), ADD FOREIGN KEY (id) REFERENCES goods_info(id))')
# conn.commit()

# # 建立表哈希表，用于存储商品信息
# detail_name = dict()
# name_map = ["跨境", "单位重量", "订货号", "加工定制", "货号", "类别", "齿轮类型", "安装形式",
#             "布局形式", "齿面硬度", "用途", "品牌", "型号", "输入转速", "输出转速范围",
#             "额定功率", "许用扭矩", "使用范围", "级数", "规格", "是否跨境出口专供货源", "减速比","传动比"
#             ]
# value_map = ["kuajing", "zhongliang", "dinghuo", "jiagong", "num", "leibie", "chilunleibie","anzhuang", 
#             "buju", "chilunyingdu", "yongtu", "pinpai", "xinghao", "shuru", "shuchu",
#             "endinggonglv", "niuju", "fanwei", "jishu", "guige", "chukou", "jiansubi", "chuangdongbi"
#             ]

# for i in range(len(name_map)):
#     detail_name[name_map[i]] = value_map[i]