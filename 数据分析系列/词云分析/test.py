import wordcloud
import wordcloud
import matplotlib.pyplot as plt
from sqlite3_model import SessionContext, GoodsDetail
import jieba

# 从GoodsDetail读取use_scope字段的数据
with SessionContext() as session:
    data = session.query(GoodsDetail.use_scope).all()
    print(data)