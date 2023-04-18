from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# 创建对象的基类:
Base = declarative_base()

# 商品数据表
class GoodsInfo(Base):
    __tablename__ = 'goods_info'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    price = Column(String(100))
    sale_sum = Column(String(100))
    link = Column(String(200))
    # 保存商品详情信息的字典
    detail = Column(String(1000))
    address = Column(String(200))
    # 厂家名称
    factory_name = Column(String(100))
    def __repr__(self):
        return "<GoodsInfo(title='%s', price='%s', sale_sum='%s', link='%s')>" % (self.title, self.price, self.sale_sum, self.link, self.detail)
    
# 商品详情数据表
class GoodsDetail(Base):
    __tablename__ = 'goods_detail'
    id = Column(Integer, primary_key=True)
    cross_bag_weight = Column(String(100))
    unit_weight = Column(String(100))
    orders_goods = Column(String(100))
    process = Column(String(100))
    num = Column(String(100))
    type = Column(String(100))
    wheel_type = Column(String(100))
    installation = Column(String(100))
    layout = Column(String(100))
    wheel_hard = Column(String(100))
    usage = Column(String(100))
    brand = Column(String(100))
    type_num = Column(String(100))
    input_rev = Column(String(100))
    output_rev = Column(String(100))
    rating_power = Column(String(100))
    allowable_torque = Column(String(100))
    use_scope = Column(String(100))
    series = Column(String(100))
    slow_ratio = Column(String(100))
    size = Column(String(100))
    sales_area = Column(String(100))
    is_brand = Column(String(100))
    is_cross = Column(String(100))
    # speed_ratio_1 = Column(String(100))
    # speed_ratio_2 = Column(String(100))
    # speed_ratio_3 = Column(String(100))
    # 额定转矩
    rating_torque = Column(String(100))
    # 额定转速
    rating_speed = Column(String(100))
    # 额定电压
    rating_V = Column(String(100))
    # 额定电流
    rating_A = Column(String(100))
    def __repr__(self):
        return "<GoodsInfo(type='%s')>" % (self.type)
    
# 链接数据库，创建数据库表
engine = create_engine('sqlite:///spider_1688_2.db', echo=True)
Base.metadata.create_all(engine)
# 创建会话
Session = sessionmaker(bind=engine)

# 使用上下文管理器管理会话
class SessionContext(object):
    def __init__(self):
        self.session = Session()
    def __enter__(self):
        return self.session
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.commit()
        self.session.close()