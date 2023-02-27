from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# 创建对象的基类
Base = declarative_base()

class GoodsInfo(Base):
    __tablename__ = 'goods_info'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(String(100))
    url = Column(String(100))
    detail = relationship('GoodsDetail', backref='goods_info')

class GoodsDetail(Base):
    __tablename__ = 'goods_detail'
    id = Column(Integer, primary_key=True)
    kuajing = Column(String(100), nullable=True, default='0')
    zhongliang = Column(String(100), nullable=True, default='0')
    dinghuo = Column(String(100), nullable=True)
    jiagong = Column(String(100), nullable=True)
    num = Column(String(100), nullable=True)
    leibie = Column(String(100), nullable=True)
    chilunleibie = Column(String(100), nullable=True)
    anzhuang = Column(String(100), nullable=True)
    buju = Column(String(100), nullable=True)
    chilunyingdu = Column(String(100), nullable=True)
    yongtu = Column(String(100), nullable=True)
    pinpai = Column(String(100), nullable=True)
    xinghao = Column(String(100), nullable=True)
    shuru = Column(String(100), nullable=True)
    shuchu = Column(String(100), nullable=True)
    endinggonglv = Column(String(100), nullable=True)
    niuju = Column(String(100), nullable=True)
    fanwei = Column(String(100), nullable=True)
    jishu = Column(String(100), nullable=True)
    guige = Column(String(100), nullable=True)
    chukou = Column(String(100), nullable=True)
    jiansubi = Column(String(100), nullable=True)
    chuangdongbi = Column(String(100), nullable=True)
    info_id = Column(Integer, ForeignKey('goods_info.id'))

# 链接数据库，创建数据库表
engine = create_engine('sqlite:///spider1688.db', echo=True)
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



