#!_*_coding:utf-8_*_

import urllib2
import re
import time
import collections

root_url = 'http://www.1kanshu.cc'
# 小说主页面

# 斗破苍穹
main_url = "http://www.1kanshu.cc/files/article/html/0/52/"

# 庶女有毒
#main_url = "http://www.1kanshu.cc/files/article/html/57/57356/"
title_page = urllib2.urlopen(main_url).read().decode('gbk').replace("\r", "").replace("\n", "").replace("\t", "")
# print title_page

title_div_list = re.findall('<div.*?id="list">(.*?)<dl>(.*?)<dt>(.*?)</dl>(.*?)</div>',title_page, re.S)

title_text = title_div_list[0][2].split('<dd>')

file_name = title_text[0].replace(u"正文</dt>", "").replace(u"《", "").replace(u"》", "")
print file_name

file_url = {}
title_list = []
for i in title_text[1:]:
    urlMap = i.replace("</a></dd>", "").replace('<a href="', "").replace('">', ':').split(":")
    title = urlMap[1]
    title_list.append(title)
    title_url = root_url + urlMap[0]
    file_url.update({title:title_url})

def get_content(title):
    try:
        content = urllib2.urlopen(file_url[title], timeout = 5).read().decode('gbk')
        content = re.findall('<div(.*?)id="content">(.*?)</div>', content)
        return content
    except:
        print u"获取数据异常，稍后重试......"
        time.sleep(5)


for title in title_list:
    count = 0
    f = open(file_name + ".txt", "ab+")
    print file_url[title]
    content = get_content(title)
    while len(content) == 0:
        time.sleep(5)
        content = get_content(title)
    print r"正在写入 " + title.encode('utf-8') + r"......"
    f.writelines("\r\n" + title.encode('utf-8') + "\r\n")
    con = content[0][1].replace("&nbsp;", " ").replace('<br />', '\r\n').encode('utf-8')
    # print con
    f.writelines(content[0][1].replace("&nbsp;", " ").replace('<div align="center"(.*?)</font>', "\r\n").replace('<br />', '\r\n').encode('utf-8'))
    f.writelines("\r\n\r\n" + u"我是分割线".center(80, "-").encode('utf-8') + "\r\n\r\n")
    f.close()
    count += 1
    if count%10 == 0:
        count = 0
        time.sleep(3)


print u"完成"