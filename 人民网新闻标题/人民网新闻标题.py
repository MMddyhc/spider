import requests
import re
import os
from bs4 import BeautifulSoup
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def getHTMLText(url):
    try:
        kv = {"user-agent":"Mozilla/5.0"}
        r = requests.get(url,headers = kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("getHTMLText失败！")
        return ""

def fillList(html,newslist):
    soup = BeautifulSoup(html, 'html.parser')
    for ul in soup.find_all("ul",class_ = "list14"):
        for li in ul.find_all("li"):
            for a in li.find_all("a"):
                newslist.append([a.text.strip(),a.get("href").strip()])
                print(a.text.strip() + "\t\t" + a.get("href").strip())

def getCloud(html,path):
    soup = BeautifulSoup(html, 'html.parser')
    news_text = ""
    for news in soup.find_all("ul",class_ = "list14"):
        news_text = "".join(news.text.strip())
    result = jieba.analyse.textrank(news_text, topK=1000000, withWeight = True)  #词频分析
    keywords = dict()
    for i in result:
        keywords[i[0]] = i[1]
    print(keywords)
    wc = WordCloud(
        font_path = r"F:\Fonts\SimHei.ttf",
        background_color="skyblue",
        max_words=50,
        width = 800,
        height = 600,
        max_font_size = 200,
        min_font_size = 2
        )
    wc.generate_from_frequencies(keywords)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    wc.to_file(path)

def main():
    newslist = []
    url = "http://www.people.com.cn/"
    path = "rmwCloud.jpg"
    html = getHTMLText(url)
    fillList(html,newslist)
    getCloud(html,path)
 
main()
