import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import string

# 读取文件
with open('textData.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 对文本进行分词
text = ' '.join(jieba.cut(text))

# 去除标点符号和停用词
punctuations = set(string.punctuation)
stopwords = set(line.strip() for line in open('stopwords.txt', encoding='utf-8'))
filter_words = [word for word in text.split() if word not in stopwords and word not in punctuations]

# 对分词结果进行词频统计
word_counts = Counter(filter_words)

# 生成词云
wordcloud = WordCloud(font_path='msyh.ttc', background_color='white', width=1200, height=1000).\
                generate_from_frequencies(word_counts)

# 显示词云
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
