#coding=utf-8
import urllib.parse
import urllib.request
import urllib.error
import random
import time
import socket 
import logging
import http.client
'''
Created on 2016年8月17日

@author: xiang
'''

class ImageUrl(object):
    '''
    下载百度图片
    '''

    def __init__(self, keyword):
        '''
        Constructor
        '''
        self.keyword=keyword
        
    
    def urlDecrypt(self, inputStr):
        '''
        url解密
        '''
        inputStr=inputStr.replace("_z2C$q", ":").replace("_z&e3B", ".").replace("AzdH3F", "/")
        intab =  "wkv1ju2it3hs4g5rq6fp7eo8dn9cm0bla"
        outtab = "abcdefghijklmnopqrstuvw1234567890"
        trantab = str.maketrans(intab, outtab)
        decryptStr=inputStr.translate(trantab)
        return decryptStr
    
    
    def getJson(self,num):
        '''
        json：获得每个图片的json
        '''
        send_headers = {
         'Host':'pic.sogou.com',
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
         'Accept':'*/*',
         'Accept-language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
         'Connection':'keep-alive',
         'Cookie':'SUV=00B72063DD7B860957BE9EEA5E3EE230; ABTEST=0|1472110316|v1; SNUID=34D33C701B1E21FB7E677CC11B2DEF05; IPLOC=CN1100; JSESSIONID=aaaXAwntLe54a43VmNaBv'
        } 
        values = {'start' : num*48, 
                  'query' : self.keyword, 
                  } 
        posturl='http://pic.sogou.com/pics?mood=0&picformat=0&mode=1&di=0&reqType=ajax&tn=0&reqFrom=result&'
        data =posturl+urllib.parse.urlencode(values)
        req = urllib.request.Request(data,headers=send_headers)
        logging.info('download url is :'+data)
        try:
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e: 
            logging.error('The server couldn\'t fulfill the request.' )
            logging.error( 'Error code: ', e.code )
        except urllib.error.URLError as e1: 
            logging.error ('We failed to reach a server.' )
            logging.error ('Reason: ', e1.reason )
        except socket.timeout as e2:
            logging.error("===========++++++++++++++++++++save "+self.keyword+str(num)+".jpg error2!===================")
            logging.error(e2)
        else:
            try: 
                page = response.read().decode("utf-8",'ignore')
            except socket.timeout as e2:
                logging.error("===========++++++++++++++++++++save "+self.keyword+str(num)+".jpg error2!===================")
                logging.error(e2)   
                return 0 
            page=str(page).strip().replace('null','\"\"').replace('true', '\"\"').replace('false', '\"\"')
            logging.debug(page[1:10])
            #print(page)
            return page
            
    def getPicUrl(self,page):
        '''
        json解析
        '''
        datas=eval(page)
        cryptUrls=[]
        for d in datas["items"]:
            if d:
                cryptUrls.append(d["pic_url"])
        #print(cryptUrls)   
        return  cryptUrls
        
        
    def savePic(self,url,num):
        '''
        picture下载图片并保存
        '''
        logging.info(url)
        #print( url[0:4])
        if(url[0:5]!='http:'):
            logging.error("===========++++++++++++++++++++save "+self.keyword+str(num)+".jpg url is error!===================")
            return
        try:      
################设置保存路径######################
            urllib.request.urlretrieve(url,'resultsg\\'+self.keyword+str(num)+'.jpg')      
        except urllib.error.URLError as e:
            logging.error("===========++++++++++++++++++++save "+self.keyword+str(num)+".jpg error0!===================")
            logging.error(e)
        except ConnectionResetError as e1:
            logging.error("===========++++++++++++++++++++save "+self.keyword+str(num)+".jpg error1!===================")
            logging.error(e1)
        except socket.timeout as e2:
            logging.error("===========++++++++++++++++++++save "+self.keyword+str(num)+".jpg error2!===================")
            logging.error(e2)
        except http.client.BadStatusLine as e3:
            logging.error("===========++++++++++++++++++++save "+self.keyword+str(num)+".jpg error3!===================")
            logging.error(e3)
def timeStamp():   
    now = int(time.time())  
    return str(now)+str(random.randrange(100, 999))


logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='runningsg.log',
                filemode='a')
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
###############################################
##############设置下载总页数和关键字##################
pageNum=300
image=ImageUrl("办公")
###############################################
socket.setdefaulttimeout(30)
picName=0
for num in range (0,pageNum,1) :
    page=image.getJson(num)
    if(page==0):
        logging.error('============================搜狗图片列表页下载失败！！！！=============================')
        continue 
    if(page[1:13]!=r'"isForbiden"'):
        logging.error('============================搜狗图片列表页下载失败！！！！=============================')
        continue   
        #print(page)                     
    cryptUrls=image.getPicUrl(image.getJson(num))
    if cryptUrls:
        for cryptUrl in cryptUrls :
            #url=image.urlDecrypt(cryptUrl)
            image.savePic(cryptUrl,picName)
            logging.info('save OK!  图片:'+str(picName))
            #print('save OK!  图片:'+str(picName))
            picName+=1
    logging.info('已下载完毕第'+str(num+1)+'页')
    #print('已下载完毕第'+str(num+1)+'页')
    time.sleep(random.randrange(3, 7))

