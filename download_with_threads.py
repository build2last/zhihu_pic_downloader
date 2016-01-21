# -*- encode:utf-8 -*-
'''
@author: Build To Last
@email: lancelotdev@163.com
mutiple threads to downloads 
'''
import urllib.parse
import urllib
from os.path import basename
import re
import urllib.request
import os
import json
import queue
import threading #多线程

#模拟浏览器访问参数
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

#用户输入链接
url=input("The full url>>")


if not os.path.exists('images'):
    os.mkdir("images")
page_size=50
offset=0
url_content=urllib.request.urlopen(url).read().decode("utf-8")
answers=re.findall('h3 data-num="(.*?)"',url_content)
limits=int(answers[0])
req=urllib.request.Request(url,headers=headers)
response=urllib.request.urlopen(req,timeout=30)
content=response.read().decode('utf8')#获取html内容转为可处理的unicode字串
#图片链接匹配规则
pic_items=re.findall('img .*?data-actualsrc="(.*?_b.*?)"',content)
print("匹配图片数目:"+str(len(pic_items))+"\n")


#多线程下载器
class download(threading.Thread):  
    def __init__(self,que):  
        threading.Thread.__init__(self)  
        self.que=que  
    def run(self):  
        while True:  
            if not self.que.empty():  
                try:
                    img_url=self.que.get()
                    req=urllib.request.Request(img_url,headers=headers)
                    img_data=urllib.request.urlopen(req,timeout=15)
                    file_name=basename(urllib.parse.urlsplit(img_url)[2])
                    with open('images/'+file_name,'wb') as pic_code:
                            pic_code.write(img_data.read())
                except:
                    print("One pic fail to download.\n")
                    print (img_url+'\n')
            else:  
                print("一个线程结束了！\n")
                break  



que=queue.Queue() 
for img in pic_items:
    que.put(img)  
for i in range(len(pic_items)):  
    d=download(que)  
    d.start()

"""
for img_url in pic_items:
    try:
        req=urllib.request.Request(img_url,headers=headers)
        img_data=urllib.request.urlopen(req,timeout=15)
        file_name=basename(urllib.parse.urlsplit(img_url)[2])
        with open('images/'+file_name,'wb') as pic_code:
                pic_code.write(img_data.read())
    except:
        print("One pic fail to download.\n")
        print (img_url+'\n')
        failures+=1
"""
if que.empty():
    print("所有线程打开结束.")
        
