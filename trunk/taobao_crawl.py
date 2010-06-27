#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Filename:tb_crawl.py
#Author: meixiaor@gmail.com
import urllib, urllib2, httplib
import socket
import os, time, random, re, sys
import threading
import Queue

from pyExcelerator import *


queue_shop_url = Queue.Queue(100)
dic_shop_url = {}
queue_item_url = Queue.Queue(500)

col_title=[r'Title',r'Art.NO', r'Size', r'Color', r'Stock', r'Price', r'LinkURL', r'ShopURL']
file_name='data.xls'

class Excel:
    '''a class to creat a excel file'''
    def __init__(self, row=0, col=0, newsheet=None):
        self.work_book=Workbook()
        self.row=row
        self.col=col
        self.sheet=newsheet
        
    def addSheet(self, sheet_name):
        self.sheet=self.work_book.add_sheet(sheet_name)

    def addRow(self, step=1):
        self.row=self.row+step
        self.col=0

    def addCol(self, step=1):
        self.col=self.col+step

    def setValue(self, i, j, value):
        self.sheet.write(i, j, value)

    def save(self, filename):
        self.work_book.save(filename)

#get the input of a excel
def get_input( queue_shop_url, filename='shop.txt'):
    global dic_shop_url
    f=file(filename, 'r')
    id=1
    while True:
        line=f.readline()
        line="".join(line.split())
        if len(line)==0:
                break
        else:
            m=re.search(r'http://(.+?).taobao.com', line)
            if m is not None:
                queue_shop_url.put((id, line))
                dic_shop_url[id]=line
                id=id+1
            else:
                print "the url is invalid,please check shop.txt!"
    if len(dic_shop_url)==0:
        print "please input at least a shop url!"

def mk_dir(parent_dir, dir):
    flag=0
    for d in os.listdir(parent_dir):
        if dir==d:
            flag=1
            break
    if flag==0:
        os.mkdir(parent_dir+os.sep+dir)
        
class Get_html(threading.Thread):
    def __init__(self, queue_shop_url, queue_item_url):
        threading.Thread.__init__(self)
        self.queue_shop_url = queue_shop_url
        self.queue_item_url = queue_item_url
        self.flag = 1
        
    def run(self):
        global  log_mutex, log_file
        while True:
            q_size = queue_shop_url.qsize()
            if q_size == 0:
                self.flag = 0
                break
            try:
#                print threading.currentThread()
                (id, shop_url) = self.queue_shop_url.get(True, 1)
            except Queue.Empty:
                break
#            print shop_url
            s_search_url=shop_url+'?search=y&price1=&price2=&pageNum=1&scid=&keyword=&orderType=_time&viewType=&isNew=&ends='
            try:
                html = urllib2.urlopen(s_search_url).read()
            except (urllib2.URLError):
                log_mutex.acquire()
                log_file.write(s_search_url+os.linesep)
                log_mutex.release()
                print "URL time out.%s"%s_search_url
                continue
            except socket.error:
                self.queue_shop_url.put((id, shop_url))
                continue
            for p in re.finditer(r'<span class="page-info">1/(\d+)</span>', html):
                page_number=p.group(1)
            #list_item_url=[]
            page_number=int(page_number)+1
#            print page_number
            for page_id in xrange(1, page_number):    
                search_url=shop_url+'?search=y&price1=&price2=&pageNum=%s&scid=&keyword=&orderType=_time&viewType=&isNew=&ends='%page_id
                try:
                    html = urllib2.urlopen(search_url).read()
                except (urllib2.URLError):
                    log_mutex.acquire()
                    log_file.write(search_url+os.linesep)
                    log_mutex.release()
                    print "URL time out.%s"%search_url
                    continue
                except  socket.error:
                    page_id = page_id -1
                    continue
#                print html
                for m in re.finditer(r'''<a href="http://item.taobao.com/item.htm\?id=(\d+?)" target="_blank">''', html):
#                    print m.group(1)
                    t_url = 'http://item.taobao.com/item.htm?id=%s'%m.group(1)
                    #g_mutex.acquire()
                    print "waiting queue size:%s"%queue_item_url.qsize()
                    self.queue_item_url.put((t_url, id))
                    if self.queue_item_url.qsize() > 300:
                        time.sleep(2)
#            print self.queue_shop_url.qsize()
            self.queue_shop_url.task_done()
        return

class Get_item(threading.Thread):
    def __init__(self, queue_item_url, dic_shop_url, thread_pool_html):
        threading.Thread.__init__(self)
        self.queue_item_url = queue_item_url
        self.dic_shop_url = dic_shop_url
        self.signal_html = thread_pool_html
        
    def is_producer_alive(self):
        flag = True
        dead_counter = 0
        for th in self.signal_html:
            if th.flag == 1:
                break
            else:
                dead_counter = dead_counter + 1
        if dead_counter == len(self.signal_html):
            flag = False
        return flag
    
    def run(self):
        global ff, f_mutex, file_name, log_mutex, log_file
        while True:
            qsize = self.queue_item_url.qsize()
            if qsize==0:
#                print self.is_producer_alive()
                if (self.is_producer_alive() == True):
                    time.sleep(0.1)
                    continue
                else:
                    break
            try:
#                print threading.currentThread()
                (url, shop_id) = self.queue_item_url.get(True, 1)
            except Queue.Empty:
                break
            try:
#                print url
                html = urllib2.urlopen(url).read()
            except (urllib2.URLError):
                log_mutex.acquire()
                log_file.write(url+os.linesep)
                log_file.flush()
                log_mutex.release()
                print "URL time out.%s"%url
                continue
            except socket.error:
                self.queue_item_url.put((url, shop_id))
                continue
            #title
            except httplib.IncompleteRead:
                self.queue_item_url.put((url, shop_id))
                continue
            m=re.search(r'<a target="_blank" href="http://item.taobao.com/spu_detail.htm\?spu_id=\d*?&no_switch=1&default_item_id=\d*?">(.*?)</a>', html)
            if m is not None:
                title=m.group(1)
                print title
            else:
                title='null'

            #art.NO
            m= re.search(r'(\d{9}|\d{6}-\d{3}|\d{4,5}-\d|\d{1}-\d{6}|\d{5,6}|[A-Z]{3}\d{3}|[A-Z|\\]{1,3}\d{3,6})', title)
            if m is not None:
                art_no=m.group(1)
                pic_name=m.group(1)
            else:
                art_no='null'
                pic_name=title
            
            size=[]
            color=[]
            stock=[]
            price=[]
#price
            m = re.search(r'<strong id="J_StrPrice" >(\d*[\.?]\d*)</strong>', html)
            if m is not None:
                price.append(m.group(1))
            else:
                price.append('null')

            for m in re.finditer(r'<li data-value="\d*:\d*"><a href="#"><span>(.*?)</span></a></li>', html):
                size.append(unicode(m.group(1), 'gbk'))

            for m in re.finditer(r'<li data-value="\d*:\d*" title="(.*?)" class="txt">', html):
                color.append(unicode(m.group(1), 'gbk'))

            if (len(size)==0) and (len(color)==0):
                size.append('null')
                color.append('null')
                m=re.search(r'<span id="J_SpanStock" class="count">(\d+)</span>', html)
                if m is not None:
                    stock.append(m.group(1))
                else:
                    stock.append('null')
            else:
                for m in re.finditer(r'"stock" : "(\d*)"', html):
                    stock.append(m.group(1))
                for m in re.finditer(r'"price" : "(\d*[\.?]\d*)"',  html):
                    price.append(m.group(1))
            #write data into excel
            vector_cross = []
            for i in size:
                for j in color:
                    vector_cross.append((i, j))
#            print size, stock, price
            f_mutex.acquire()
            for (i_size, i_color), i_stock, i_price in zip(vector_cross, stock, price):
                ff.addRow()
                ff.setValue(ff.row, ff.col, unicode(title, 'gbk'))
                ff.addCol()
                ff.setValue(ff.row, ff.col, art_no)
                ff.addCol()
                ff.setValue(ff.row, ff.col, i_size)
                ff.addCol()
                ff.setValue(ff.row, ff.col, i_color)
                ff.addCol()
                ff.setValue(ff.row, ff.col, i_stock)
                ff.addCol()
                ff.setValue(ff.row, ff.col, i_price)
                ff.addCol()
                ff.setValue(ff.row, ff.col, url)
                ff.addCol()
                ff.setValue(ff.row, ff.col, dic_shop_url[shop_id])
            ff.save(file_name)
            f_mutex.release()

            self.queue_item_url.task_done()
        return
            #crawl picture 

if __name__ == '__main__':
    global f_mutex, ff, log_mutex, log_file
#    socket.setdefaulttimeout(10)
    start = time.clock()
    print "Ready to crawl infomation from Taobao!"
    ff = Excel()
    ff.addSheet("Sheet1")
    
    log_file = file('error.txt', 'w+')
    log_mutex = threading.Lock()
    for i in col_title:
        ff.setValue(ff.row, ff.col, i)
        ff.addCol()

    thread_pool_html = []
    thread_size_html = 2

    thread_pool_item = []
    thread_size_item = 20
    
    f_mutex = threading.Lock()
    get_input(queue_shop_url)

#    print queue_shop_url
    for i in xrange(thread_size_html):
        t=Get_html(queue_shop_url, queue_item_url)
        t.setDaemon(True)
        thread_pool_html.append(t)
        t.start()

    #thread used for crawling item info from item url
    for i in xrange(thread_size_item):
        th=Get_item(queue_item_url, dic_shop_url,thread_pool_html)
        th.setDaemon(True)
        thread_pool_item.append(th)
        th.start()
    queue_shop_url.join()
    queue_item_url.join()
    end = time.clock()
    
    log_file.flush()
    log_file.close()
    print "exec time %s s."%(end-start)
    print "OK,please check the generated excel files!"
