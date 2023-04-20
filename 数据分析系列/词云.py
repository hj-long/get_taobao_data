import wordcloud
import matplotlib.pyplot as plt
from sqlite3_model import SessionContext, GoodsDetail
import jieba

# 从GoodsDetail读取use_scope字段的数据
with SessionContext() as session:
    data = session.query(GoodsDetail.use_scope).all()
    # 文本数据
    text = ''
    for item in data:
        if item[0] is not None:
            # item[0]格式为 食品、纺织、冶金 或者 撕碎机,皮带机，矿山设备，电厂，水泥厂 需要去除逗号和数字，并且分词
            if item[0].isdigit():
                continue
            text += ' '.join(jieba.cut(item[0].replace(',', '').replace('，', '').
                                       replace('、', '').replace('等行业', '').replace('等领域', '').replace('等', '').
                                            replace('等', '').replace(' ', '').replace('（', '').replace('）', '').
                                                replace('(', '').replace(')', '')))

    print(text)
    # 生成词云
    wc = wordcloud.WordCloud(
            font_path='C:\Windows\Fonts\simhei.ttf', width=1000, height=800, background_color='white',
            collocations=False
        )
    wc.generate(text)
    # 保存图片
    wc.to_file('use_scope.png') 
    
    # 显示图片
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
                
