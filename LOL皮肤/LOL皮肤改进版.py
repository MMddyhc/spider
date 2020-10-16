import requests
import re
import os
from bs4 import BeautifulSoup

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

def fillList(skinlist,url):
    for i in range(1, 4):      #皮肤展示页面共43页
        new_url = url + "hero_{}.shtml".format(i)   #拼出每个页面url
        html = getHTMLText(new_url)
        soup = BeautifulSoup(html, features = 'html.parser')
        div_soup = soup.find('div', class_ = 'ListBigContent')
        lis = div_soup('li')    #查询li标签

        for li in lis:
            skin_url = li.find('a', target='_blank')
            skin_url = skin_url.get("href")
            skinlist.append(skin_url)
        print("页面{0}解读完毕!".format(i))
            
def getImageAddress(skinlist,nameAndImage):
    for url in skinlist:
        html = getHTMLText(url)
        soup = BeautifulSoup(html, features = 'html.parser')
        name_div = soup.find('div', class_ = 'pifuIntroText pifuIntroText2')
        hero_name = name_div.find('h2').text
        skin_name = name_div.find('h1').text
        name = hero_name.strip() + '-' + skin_name.strip()
        name = name.replace('/', '')    #把字符中的"/"替换成空，否则会影响路径，都是K/DA的锅
        image_div = soup.find('div', class_ = 'pifuIntroPic pifuIntroPic2')

        image_url = image_div.find('img')
        image_url = image_url.get('src')
        nameAndImage.append([name,image_url])
        print("{0}链接已获取!".format(name))
    
def getImage(path,nameAndImage):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        for i in range(len(nameAndImage)):
            save_path = os.path.join(path, nameAndImage[i][0]+'.jpg')
            url = nameAndImage[i][1]
            r = requests.get(url)
            if not os.path.exists(save_path):
                image = r.content
                with open(save_path, 'wb') as f:
                    f.write(image)
                print('{}保存成功!'.format(nameAndImage[i][0]))
            else:
                print('{}已存在'.format(nameAndImage[i][0]))  
    except Exception as e:
        print('{}保存失败'.format(nameAndImage[i][0]),e)


def main():
    skinlist = []
    nameAndImage =[]
    path = "./image" 
    url = "http://lol.52pk.com/pifu/hero/"
    fillList(skinlist,url)
    print("fillList成功")
    getImageAddress(skinlist,nameAndImage)
    print("getImageAddress成功")
    getImage(path,nameAndImage)
    print("getImage成功")

main()
