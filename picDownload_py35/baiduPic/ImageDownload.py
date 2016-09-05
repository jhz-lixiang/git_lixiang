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
         'Host':'image.baidu.com',
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
         'Connection':'keep-alive',
         'Cookie':'BDqhfp=%E5%AE%A0%E7%89%A9%26%260-10-1undefined%26%262706%26%265; BAIDUID=2BD68F7BEF1EFD5B1E80A0B804D3890F:FG=1; BIDUPSID=BD9AC8F8C1029E83D09FDF70D1247338; PSTM=1471507960; H_PS_PSSID=1425_18282_17947_12047_20857_20836_20770; BDRCVFR[Fc9oatPmwxn]=G01CoNuskzfuh-zuyuEXAPCpy49QhP8; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; userFrom=www.baidu.com; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm'
        } 
        values = {'ct' : '201326592', 
                  'queryWord' : self.keyword, 
                  'word' : self.keyword,
                  'pn' : num*30,
                  'rn' : '30',
                  'gsm' : '3c',
                  timeStamp() : ''
                  } 
        posturl='http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&is=&fp=result&cl=&lm=&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&'
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
            logging.error("===========++++++++++++++++++++save f:\\picture\\"+self.keyword+str(num)+".jpg error2!===================")
            logging.error(e2)
        else:
            try: 
                page = response.read().decode('utf-8').replace('null','\"\"')
            except socket.timeout as e2:
                logging.error("===========++++++++++++++++++++save f:\\picture\\"+self.keyword+str(num)+".jpg error2!===================")
                logging.error(e2)   
                return 0 
            logging.debug(page[1:10])
            return page
            
    def getPicUrl(self,page):
        '''
        json解析
        '''
        datas=eval(page)
        cryptUrls=[]
        for d in datas["data"]:
            if d:
                cryptUrls.append(d["objURL"])
        #print(cryptUrls)   
        return  cryptUrls
        
        
    def savePic(self,url,num):
        '''
        picture下载图片并保存
        '''
        logging.info(url)
        try:      
################设置保存路径######################
            urllib.request.urlretrieve(url,'result1\\'+self.keyword+str(num)+'.jpg')      
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
                filename='running.log',
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
image=ImageUrl("餐厅")
###############################################
socket.setdefaulttimeout(30)
picName=0
for num in range (0,pageNum,1) :
    page=image.getJson(num)
    if(page==0):
        logging.error('============================百度图片列表页下载失败！！！！=============================')
        continue 
    if(page[1:11]!=r'"queryEnc"'):
        logging.error('============================百度图片列表页下载失败！！！！=============================')
        continue                        
    cryptUrls=image.getPicUrl(image.getJson(num))
    if cryptUrls:
        for cryptUrl in cryptUrls :
            url=image.urlDecrypt(cryptUrl)
            image.savePic(url,picName)
            logging.info('save OK!  图片:'+str(picName))
            #print('save OK!  图片:'+str(picName))
            picName+=1
    logging.info('已下载完毕第'+str(num+1)+'页')
    #print('已下载完毕第'+str(num+1)+'页')
    time.sleep(random.randrange(3, 7))

