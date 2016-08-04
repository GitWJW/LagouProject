#coding=utf-8

import jieba
from wordcloud import WordCloud
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8') 

f = open('/home/wjw/pythonProject/lagouProject/alldata.txt','r')
content = f.read()
f.close()

s = {}
contents = jieba.cut(content)
for w in contents:
    if len(w)>1:
        pre_count = s.get(w,0)
        s[w] = pre_count+1
   
words = sorted(s.iteritems(),key=lambda d:d[1], reverse = True)
words = words[1:100]

wordclouds = WordCloud(font_path='/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc').fit_words(words)
import matplotlib.pyplot as plt
plt.imshow(wordclouds)
plt.axis('off')
plt.show()

