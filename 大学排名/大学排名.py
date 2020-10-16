import requests
import re
import bs4
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("getHTMLText失败！")
        return ""

def fillUnivList(ulist,html):
    soup = BeautifulSoup(html,"html.parser")
    for tr in soup.find("tbody").children:
        if isinstance(tr,bs4.element.Tag):      #过滤非标签信息
            tds = tr("td")      #查询td标签
            tagas = tr("a")     #查询a标签
            ulist.append([tds[0].string.strip(),tagas[0].string.strip(),tds[2].string.strip(),tds[3].string.strip(),tds[4].string.strip()])
    pass

def printUnivList(ulist,num):
    a = "{0:^10}{1:{5}^10}{2:^10}{3:^10}{4:^10}"
    print(a.format("排名","学校","地域","类型","总分",chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(a.format(u[0],u[1],u[2],u[3],u[4],chr(12288)))

def save(path,ulist):
    Excel = open(path,'w',encoding = 'gbk')
    Excel.write('排名\t学校\t地域\t类型\t总分\n')
    for i in range(len(ulist)):
        for j in range(len(ulist[i])):
            Excel.write(str(ulist[i][j]))
            Excel.write('\t')      #相当于Tab一下，换下一个单元格
        Excel.write('\n')          #写完一行，换行
    Excel.close()

def main():
    uinfo = []
    url = "http://www.shanghairanking.cn/rankings/bcur/2020.html"
    html = getHTMLText(url)
    print("get成功")
    fillUnivList(uinfo,html)
    print("fill成功")
    printUnivList(uinfo,20)     #20univs
    print("print成功")
    save("大学排名.xls",uinfo)
    print("save成功")

main()
    
