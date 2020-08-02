#!/usr/bin/python3

import os
import getpass
import random
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

class Water_Automaton:
    def __init__(self,home="宫漫"):
        try:#读取设置好的评论文本
            self.cnt=len(os.listdir('./'+home))
            self.texts=["" for i in range(self.cnt)]
            i=0
            while i<self.cnt:
                fp=open(home+'/'+str(i)+'.txt','r',encoding='UTF-8')
                self.texts[i]=fp.read()
                fp.close()
                i=i+1
            pass
        except:#如果没有文本就经验加三
            self.cnt=1
            self.texts=["经验加三，告辞"]
            pass
        option = webdriver.ChromeOptions()
        option.add_argument(r'./chromedriver.exe')
        username=getpass.getuser()
        if os.path.exists(r"C:\Users\Hasee"):
            username="Hasee"
        option.add_argument(r"user-data-dir=C:\Users\\"+username+r"\AppData\Local\Google\Chrome\User Data")#获取浏览器数据
        self.driver=webdriver.Chrome(options=option)#打开浏览器
        self.__ba=home
        self.__ba_url="https://tieba.baidu.com/f?kw="+home
        
    def Send(self,driver,url,words):#发帖
        try:
            driver.get(url)
            driver.find_element_by_xpath('/html').send_keys(Keys.END)
            sleep(1.5)
            driver.find_element_by_id('ueditor_replace').send_keys(words)
            sleep(1.5)
            driver.find_element_by_link_text('发 表').click()
            sleep(3)
            pass
        except:
            pass

    def GetComment(self,driver,url):#获取帖子的回复
        try:
            driver.get(url)
            lst=driver.find_elements_by_xpath(r'.//div[@class="d_post_content j_d_post_content " and @id]')
            sz=len(lst)
            re=["" for i in range(sz)]
            i=0
            while i<sz:
                re[i]=lst[i].text
                i=i+1
            return re
        except:
            return {}

    def GetUrl(self,driver,url):#获取吧主页的所有帖子
        try:
            driver.get(url)
            lst=driver.find_elements_by_xpath(r'.//a[@rel="noreferrer" and @class="j_th_tit "]')
            sz=len(lst)
            re=["" for i in range(sz)]
            i=0
            while i<sz:
                re[i]=lst[i].get_attribute('href')
                i=i+1
            return re
        except:
            return {}
    
    def handle_tie(self,driver,url):#处理一个帖子
        comments=self.GetComment(driver,url)
        sz=len(comments)
        if sz<2 or human=='n' or random.randint(1,3)==2:#当该贴有人回复时 则有2/3的概率复读; 如果没有选择复读模式 则不复读
            words=self.texts[random.randint(0,self.cnt-1)]
            print(words)
            self.Send(driver,url,words)
            return
        else:
            words=comments[random.randint(0,sz-1)]
            print(words)
            self.Send(driver,url,words)
            return
        
    def handle_page(self,url,bomb='n'):#处理一个主页
        urls=self.GetUrl(self.driver,url)
        print(urls)
        for ele in urls:
            self.handle_tie(self.driver,ele)
            if bomb=='n':
                tm=random.randint(0,9)
                sleep(tm)#如需炸吧，就不执行时间缓冲
                
    def Run(self,limit=1,bomb='n'):
        try:
            print(self.__ba_url)
            i=0
            while i<limit:
                self.handle_page(self.__ba_url+'&ie=utf-8&pn='+str(i*50),bomb)#每次翻一页
                i+=1
            self.driver.quit()
            pass
        except:
            return

if __name__ == '__main__' :
    word=input('输入吧名:')
    lim=int(input('终止页数:'))
    bmb=input('是否炸吧?[y/n]')
    human=input('是否复读?[y/n]')
    xp=Water_Automaton(word)
    xp.Run(lim,bmb)
