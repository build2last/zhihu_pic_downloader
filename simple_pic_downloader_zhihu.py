#-*- encoding:utf-8 -*-
'''
@author: Build To Last
@email: lancelotdev@163.com
auto make folder named with the question
'''
import urllib.parse
import urllib
from os.path import basename
import re
import urllib.request
import os
import json
from macpath import dirname

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
failures=0
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
print("匹配到的图片数目:"+str(len(pic_items))+"\n")

#添加功能，根据问题自命名目录
title_pattern=re.compile("<title>(.+?)</title>", re.S)
title_re=re.findall(title_pattern, content)
the_dirname=u''
if len(title_re)==1:
    the_dirname=str(title_re[0]).strip()
    the_dirname =  re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]","",the_dirname)
    os.mkdir("images/"+the_dirname)
#
for img_url in pic_items:
    try:
        req=urllib.request.Request(img_url,headers=headers)
        img_data=urllib.request.urlopen(req,timeout=15)
        file_name=basename(urllib.parse.urlsplit(img_url)[2])
        with open('images/'+the_dirname+'/'+file_name,'wb') as pic_code:#添加功能，根据问题自命名目录
                pic_code.write(img_data.read())
    except:
        print("One pic fail to download.\n")
        print (img_url+'\n')
        failures+=1
        
print("结束，失败数："+str(failures))
