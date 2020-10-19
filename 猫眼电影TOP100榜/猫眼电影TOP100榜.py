import requests
import re
import os
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        kv = {
            "user-agent":"Mozilla/5.0",
            "Cookie": "__mta=150238857.1602895907970.1602895907970.1602895907970.1; uuid_n_v=v1; uuid=EF37CF40101211EBA49537871E07CB9B551E0E6AAAD0496CB9577D92C804414F; _csrf=48c1a11d90da9b55c99273c2bbc35e938aec46d79119cc219fd139828fd29bde; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1602895908; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1602895908; _lxsdk_cuid=175340a8c37c8-02b1af385c3412-5373e62-144000-175340a8c373c; _lxsdk=EF37CF40101211EBA49537871E07CB9B551E0E6AAAD0496CB9577D92C804414F; _lxsdk_s=175340a8c39-48c-9f6-8fe%7C%7C2"
            }
        r = requests.get(url,headers = kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("getHTMLText失败！")
        return ""

def fillList(url,pagelist):
    for i in range(10):
        new_url = url + "{}".format(i*10)
        pagelist.append(new_url)

def getAndSave(pagelist,path):
    with open(path,'a',encoding = 'utf-8') as f:
        for page in pagelist:
            html = getHTMLText(page)
            soup = BeautifulSoup(html,"html.parser")
            for dd in soup.find_all('dd'):
                plist = []
                for p in dd.find_all('p'):
                    plist.append(p.string)
                f.write(dd.i.string + '\t' + plist[0].strip() + '\t' + plist[1].strip() + '\t' + plist[2].strip() + '\t' + 'http://maoyan.com' + dd.p.a['href'] + '\n')
                print(dd.i.string + "\t" + plist[0].strip())
    f.close()
    
def main():
    pagelist = []
    url = "https://maoyan.com/board/4?offset="
    path = "猫眼TOP100.txt"
    fillList(url,pagelist)
    print("fill成功")
    getAndSave(pagelist,path)
    print("save成功")

main()
