#coding=utf-8
import codecs  
import time
import os
import logging
import threading
import urllib.request
import urllib.error
import socket
import http

'''
Created on 2016年8月29日

@author: xiang
'''

class MyThread(threading.Thread):
    """docstring for MyThread"""

    def __init__(self, url,picname,newurlfilename1,newurlfilename2,threadLock1,threadLock2) :
        super(MyThread, self).__init__()  #调用父类的构造函数 
        self.url = url
        self.picname = picname
        self.newurlfilename1=newurlfilename1
        self.newurlfilename2=newurlfilename2
        self.threadLock1=threadLock1
        self.threadLock2=threadLock2

    def run(self) :
        if(downloadpic(self.url,self.picname)):
            self.threadLock1.acquire() #获取锁
            self.newurlfilename1.write(self.picname+'\t'+self.url)
            self.threadLock1.release() #释放锁
        else:
            self.threadLock2.acquire() #获取锁
            self.newurlfilename2.write(self.picname+'\t'+self.url)
            self.threadLock2.release() #释放锁
            #time.sleep(1)
                    
'''
url列表写入文件
'''
def writeullist(urls,filename):
    newurlfilename=codecs.open(filename,'a',"utf-8")
    for key in urls.keys():
        newurlfilename.write(key+'\t'+urls[key]+'\n')
    newurlfilename.close()
    
'''
读入已下载过的url列表文件
'''
def readurllist(urlfileName):
    time1=time.time()
    logging.info('开始读url列表文件的时间为：'+str(time.ctime(time1)))
    urls=open(urlfileName,'rb')
    dict1={}
    for line in urls.readlines():
        strs=line.decode('utf-8','ignore').split('\t')
        #print(strs)
        dict1[strs[0]]=strs[1]
    time2=time.time()
    logging.info('读取url列表文件完成的时间为：'+str(time.ctime(time2))) 
    logging.info('读取全部url耗时'+str(time2-time1)+'秒\n'  )
    urls.close()
    return dict1

'''
判断文件的大小
'''
def samefileSize(file1,file2):
    if(os.path.getsize(file1)==os.path.getsize(file2)):
        return True
    else:
        return False

'''
下载新的图片url列表页文件并将原有的备份
'''
def downloadNewUrllist():
    newNum=111
    #####下载网站上图片数量
    lastTimeNum=open('filenums.txt','rb')
    for line in lastTimeNum.readlines():
        str=line.decode('utf-8','ignore')
        if(str==newNum):
            lastTimeNum.close()
            return 0
        else:
            lastTimeNum.close()
            lastTimeNum=codecs.open('filenums.txt','w',"utf-8")
            lastTimeNum.write(newNum)
            lastTimeNum.close()
            ######下载文件
            return 1
        
'''
获得未下载图片url列表
'''
def undownloadPic(newfilename, savedfilename):
    newurldict=readurllist(newfilename)
    try:
        urls=open(savedfilename,'rb')
        for line in urls.readlines():
            strs=line.decode('utf-8','ignore').split('\t')
            print(strs)
            newurldict.pop(strs[0])
        urls.close()
    except FileNotFoundError as e:
        logging.error("文件saved.txt不存在")
        logging.error(e)
    return newurldict

'''
多线程下载或跳过图片
'''
def downloadAll(threadnum,undownloadDict,savedDict,failedDict):
    threadpool=[]
    threadLock1 = threading.Lock()
    threadLock2 = threading.Lock()
    keys= list(undownloadDict.keys())
    logging.info('保存未下载数据的id共'+str(len(undownloadDict))+'条')
    
    i=0
    num=len(undownloadDict)
    while i<num:
        j=0
        logging.info('下一组下载数据起始于'+str(i))
        #time.sleep(5)
        while j<threadnum and i+j < num:
            #得到一个网址
            picname=keys.pop()
            url=undownloadDict[picname]
            logging.info('待下载picname is :'+picname+'\turl is :'+url)
            myThread=MyThread(url,picname,savedDict,failedDict,threadLock1,threadLock2)
            threadpool.append(myThread)
            myThread.start( )
            j+=1
        i+=j
        for thread in threadpool:
            thread.join(30)
        threadpool=[]
    #logging.info('共下载数据'+str(num)+'条， 下载成功数据'+str(count1)+'条，下载失败数据'+str(count2)+'条')    
'''
picture下载图片并保存
''' 
def downloadpic(url,picname):
    logging.info(url)
    try:      
################设置保存路径######################
        req=urllib.request.urlretrieve(url,picname+'.jpg')    
        print(req)
    except urllib.error.URLError as e:
        logging.error("===========++++++++++++++++++++save "+picname+".jpg error0!===================")
        logging.error(e)
        return False
    except ConnectionResetError as e1:
        logging.error("===========++++++++++++++++++++save "+picname+".jpg error1!===================")
        logging.error(e1)
        return False
    except socket.timeout as e2:
        logging.error("===========++++++++++++++++++++save "+picname+".jpg error2!===================")
        logging.error(e2)
        return False        
    except http.client.BadStatusLine as e3:
        logging.error("===========++++++++++++++++++++save "+picname+".jpg error3!===================")
        logging.error(e3)
        return False
    return True

##########配置log
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='running.log',
                filemode='a')
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
###########设置socket超时时间
socket.setdefaulttimeout(30)
'''
time1=time.time()
print( time.ctime(time1 ))
savedict={}
faileddict={}
undownloaddict=undownloadPic('f:\\new.txt', 'saved.txt')
newurlfilename1=codecs.open('saved.txt','a',"utf-8")  
newurlfilename2=codecs.open('failed.txt','a',"utf-8")
downloadAll(60,undownloaddict,newurlfilename1,newurlfilename2)
newurlfilename1.close() 
newurlfilename2.close()
time2=time.time()
logging.info( time.ctime(time2 ))
logging.info ('读取全部url耗时'+str(time2-time1)+'秒\n'  )
'''

downloadpic('http://pic2.nipic.com/20090505/2091217_114855009_2.jpg','aaa')