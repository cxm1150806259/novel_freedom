#-*-coding:utf-8 -*-
from urllib import request
import urllib.response
from bs4 import BeautifulSoup
import re
import sys
import time


if __name__ == "__main__":                             #新笔趣阁
    #创建txt文件
    file = open('百炼飞升录.txt','w',encoding='utf-8')
    #小说目录地址
    target_url = 'https://www.xxbiquge.com/4_4808/'
    # User-Agent
    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    target_req = request.Request(url = target_url,headers = head)
    target_response = request.urlopen(target_req)
    target_html = target_response.read().decode('utf-8')

    # print(target_html)
    #创建BeautifulSoup对象
    listmain_soup = BeautifulSoup(target_html,'html.parser')
    # file.write(str(listmain_soup.find_all()))
    # file.close()
    # print(listmain_soup)
    #搜索文档树，找出div标签中class为listmain的所有子标签
    chapters = listmain_soup.find_all('div',class_ = 'box_con')
    # print(chapters[1])
    #使用查询结果再创建一个BeautifulSoup对象，对其继续进行解析
    download_soup = BeautifulSoup(str(chapters[1]),'lxml')
    # print(download_soup)

    #章节个数
    numbers = len(download_soup.dl.contents) - 5
    print(numbers)
    index = 1

    #开始记录内容标志位，只要正文卷下面的链接，最新章节列表链接剔除
    begin_flag = False
    #记录开始时间
    print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))


    #遍历dl标签下所有子节点
    for child in download_soup.dl.children:
        #滤除回车
        if child != '\n':
            #找到《一念永恒》正文卷，使能标志位
            if child.string == u"《百炼飞升录》正文":
                begin_flag = True
            if begin_flag == True and child.a != None:
                download_url = target_url + child.a.get('href').split('/')[2]

                download_req = request.Request(url = download_url, headers = head)
                download_response = request.urlopen(download_req)
                download_html = download_response.read().decode('utf-8','ignore')
                download_name = child.string
                # print("%s:%s"%(download_name,download_url))
                soup_texts = BeautifulSoup(download_html,'lxml')
                texts = soup_texts.find_all('div',id = 'content')
                soup_text = BeautifulSoup(str(texts),'lxml')
                write_flag = True
                enter_flag = True
                file.write(download_name+'\n\n')
                #将爬取内容写入文件,\xa0为空白符&nbsp
                for each in soup_text.div.text.replace('\xa0','\r'):
                    if each == 'h':
                        write_flage = False
                    if write_flag == True and each != '\r':
                        file.write(each)
                        enter_flag = False
                    if write_flag == True and enter_flag == False and each == '\r':
                        file.write('\n')
                        enter_flag = True
                file.write('\n\n')
                #打印爬取速度
                print("已下载:%.3f%%" % float(index/numbers) + '\r')
                # sys.stdout.write("已下载:%.3f%%" % float(index/numbers) + '\r')
                # sys.stdout.flush()
                index += 1
    file.close()
    # 记录结束时间
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
















