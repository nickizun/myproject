import time

from lxml import etree
import requests
import re
import os
import socket
socket.setdefaulttimeout(20)

headers={
   'user_agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 SLBrowser/7.0.0.6241 SLBChan/103'
}
def main_page_findhua(url):
    new_response=requests.get(url,headers=headers)
    newhtml=new_response.text
    new_xpath=etree.HTML(newhtml)
    hua_urls= new_xpath.xpath('/html/body/div[5]/div/div/div[2]/ul/li/h3/a/@href')
    return hua_urls

def find_urls(html):
    urls = re.findall(r'zoomfile="(.*?)"', html)
    return urls


def storge_pictures(html):
    num = 1
    urls = find_urls(html)
    name = re.findall(r'<span id="thread_subject">【韩漫】寄宿日记:(.*?)<', html)[-1]
    if not os.path.exists(name):
        os.mkdir(name)
    i = 0
    for url in urls:
        try:
            print(url)
            i = i + 1
            file_name = str(i) + '.jpg'
            stor(url, i, name)
            time.sleep(3)
        except:
            if not num == 4:
                num = num + 1
                stor(url, i, name)


def stor(url, i, name):
    file_name = str(i) + '.jpg'
    response = requests.get(url, headers=headers)
    with open(name + '/' + file_name, 'wb') as fp:
        fp.write(response.content)
    response.close()


def enter_hua(url):
    response = requests.get(url,headers=headers)
    html = response.text
    storge_pictures(html)






response=requests.get('https://rewrfsrewr.xyz/search.php?mod=forum&searchid=369287&orderby=lastpost&ascdesc=desc&searchsubmit=yes&page=1',headers=headers)

html=response.text
res_xpath=etree.HTML(html)
page_urls=res_xpath.xpath('//*[@id="ct"]/div/div/div[3]/div/a/@href')
page_urls.pop()
page_urls.insert(0,'https://rewrfsrewr.xyz/search.php?mod=forum&searchid=369287&orderby=lastpost&ascdesc=desc&searchsubmit=yes&page=1')

for main_page in page_urls:
    print(main_page)
    hua_urls=main_page_findhua('https://rewrfsrewr.xyz/'+main_page)
    print('https://rewrfsrewr.xyz/'+main_page)
    for hua in hua_urls:
       response=requests.get('https://rewrfsrewr.xyz/'+hua,headers=headers)
       nowhtml = response.text
       storge_pictures(nowhtml)