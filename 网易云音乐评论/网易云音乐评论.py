import requests
import re
import os
from bs4 import BeautifulSoup
import json
# http://music.163.com/api/v1/resource/comments/R_SO_4_569213220?limit=100&offset=0

def getHTMLText(url):
    try:
        kv = {"user-agent":"Mozilla/5.0"}
        r = requests.get(url,headers = kv)
        r.raise_for_status()
        #r.encoding = r.apparent_encoding
        return r.text
    except:
        print("getHTMLText失败！")
        return ""

def fillList(music_id,url,commentlist):
    for i in range(4):
        new_url = url + "{0}?limit=100&offset={1}".format(music_id,100*i)
        print(new_url)
        html = getHTMLText(new_url)
        json_dict = json.loads(html)        #利用json方法把json类型转成dict
        comments = json_dict['comments']
        for item in comments:
            try:
                commentlist.append([item['user']['nickname'],item['content']])
                print(item['user']['nickname'] + "评论了：" + item['content'])
            except:
                print("特殊字符打印失败！！！")

def save(commentlist,path):
    with open (path,'a',encoding = 'utf-8') as f:
        for comment in commentlist:
            f.write(comment[0] + "评论了: " + comment[1] + "\n")
    f.close()

def main():
    music_id = "569213220"
    url = "http://music.163.com/api/v1/resource/comments/R_SO_4_"
    commentlist = []
    path = "像我这样的人.txt"
    fillList(music_id,url,commentlist)
    save(commentlist,path)
    
main()
