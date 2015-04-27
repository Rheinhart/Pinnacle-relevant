# -*- coding: utf-8 -*-
import urllib2
import urllib
import cookielib
import sys
import bs4
import re
import requests
from PIL import Image  #handle the image
import os

######
reload(sys)
sys.setdefaultencoding("utf8")
######
login_url = 'https://aaa.pinnaclesports.com/Login.aspx'
pinnacle_session = requests.Session()
class PinnacleLogin():
    """Automatically login the Pinnacle to get the data of Balance Sheet"""
    def __init__(self):

        self.username = ''
        self.password = ''
        self.pinnacle_balance = ''
        self.balance_sheet = {} #result saved in this table
        self.captcha_url = ''
        self.header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                  'Cache-Control':'max-age=0',
                  'Connection':'keep-alive',
                  'Content-Type':'application/x-www-form-urlencoded',
                  'DNT':'1',
                  'Host':'aaa.pinnaclesports.com',
                  'Origin':'https://aaa.pinnaclesports.com',
                  'Referer':'https://aaa.pinnaclesports.com/Login.aspx',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}


    def set_login_info(self,username,password):
        '''set the user information'''
        self.username = username
        self.password = password

    def _loginmain(self):
        '''login the main page'''
        postData = {'__VIEWSTATE':'/wEPDwUINDc3MzExNzIPZBYCAgMPZBYCAgEPZBYCAgMPEGQPFgECBxYBEAUEVGhhaQUCdGhnFgFmZGRevYPRLil7tSWwrGv94kOQWgS/Z/UdYWX+2Psw3JdwrQ==',
            '__VIEWSTATEGENERATOR':'C2EE9ABB',
            '__EVENTVALIDATION':'/wEdAA0XhIbGiuWL6wNXsuKKNl9+zyjSCk071VEBFi+Pn+x7Vbskj2bYtjy6x+ok0AhsxbmaWJgNYxXDKJmfHo3SUAtyDajVEjtqqAB+Fe3DJW2ReMqDhLSZLEX/ZvMqb4F5bexjIsOsOCcsfe6l6fcRigHQEAWAfkf0gHlvWmxI/1mZHAgsYlVDpoodEWRg9RRToQqwRQmdYVIGdQOw5ctONxUqR1LBKX1P1xh290RQyTesRVwK8/1gnn25OldlRNyIednDbiWC8p5oWQ9KZC32jRIUQPgwUS8va+KcSB9QJ0dkZouFlD3gerUhEyV9P/WYD/o=',
            'UPBF$LDDL':'en-GB',
            'UserName': self.username,
            'Password': self.password,
            'LB':'Login'}

        req = pinnacle_session.post(login_url, postData,headers=self.header,timeout=60*4)

        try:
            content = str(req.content)
        except  urllib2.HTTPError, e:
            print e.code

    def _kickoff(self):
        '''kick off other user and continue'''

        kickoff_url = 'https://aaa.pinnaclesports.com/AlreadyLoggedIn.aspx'

        postData = {'__VIEWSTATE':'/wEPDwULLTEzMDIzODIwMTNkZOmQJfUJyJT5fL5xtNAp2w1JEhyndb8AJjxA3GoJBox8',
        '__VIEWSTATEGENERATOR':'9461229B',
        '__EVENTVALIDATION':'/wEdAAXI5Cf5IjAXLSFBNsvmq/sRUbCimvzN/TczT4kz9qKpYnFNg25++/wnLLvx/zMOPgtg4wULag6puEpGFyFXlupb70/AcP6TbUveJn5MuDyMx7c9aL0zH/wbg+CtvVsRp1Fi1jTGdqVURYr7DEN6f2Fe',
        'LIHF': self.username,
        'LPHF': self.password,
        'COB':'Continue'}

        req = pinnacle_session.post(kickoff_url, postData,headers=self.header,timeout=60*20)
        try:
            self.pinnacle_balance = str(req.content)
        except  urllib2.HTTPError, e:
            print e.code

        tag = 'Yesterday Total Balance'
        if  re.search(tag,self.pinnacle_balance):
            #login successful
            print 'Logged in successfully!\n'
        else:
            #login failure
            print 'Logged in failed, check result.html file for details\n'

    def _parserpage(self):

        #print 'parser the page...'
        soup = bs4.BeautifulSoup(self.pinnacle_balance)
        #select the content between tags of 'td' in outer tag 'tr'
        balanceData = soup.select('tr.MTR1 td')

        for i in range(0,balanceData.__len__()-1,2):
            self.balance_sheet[re.sub('^CNY ','',str(bs4.BeautifulSoup(str(balanceData[i])).get_text()))] = re.sub('^CNY ','',str(bs4.BeautifulSoup(str(balanceData[i+1])).get_text()))
        for (k,v) in self.balance_sheet.items():
            print "%s: %s\n" % (k,v)

    def _savedata(self):
        """save the data"""
        sName = 'C:\\Users\\taoju\\Desktop\\'+'pinnacle_balance' + '.txt'
        try:
            f = open(sName,'w')
            for (k,v) in self.balance_sheet.items():
                f.write("%s: %s\n" % (k,v))
            f.close()
            print 'balance_sheet saved in the dictionary ' + sName + '......'
        except IOError:
            print "Cannot create the file!"

    def _getcaptchaurl(self):

        url = 'https://aaa.pinnaclesports.com/Members/NewMember.aspx'
        getCode = pinnacle_session.get(url,timeout=60*20)
        str = getCode.content
        sName = 'C:\\Users\\taoju\\Desktop\\'+'pinnacle_newmember' + '.txt'
        f = open(sName,'w')
        f.write(str)
        f.close()

        captcha_url_postfix = re.findall("CaptchaHandler\.ashx\?cc=(.*)\"",str)
        self.captcha_url = 'https://aaa.pinnaclesports.com/UserControls/CaptchaApp/CaptchaHandler.ashx?cc='+captcha_url_postfix[0]
        print captcha_url_postfix[0]

    def _getnewpostdata(self):
        str = open()
    def _getcaptcha(self):

        self._getcaptchaurl()
        capr = pinnacle_session.get(self.captcha_url,timeout=60*20)
        with open('C:\\Users\\taoju\\Desktop\\captcha_newmember.png', 'wb') as f:
            f.write(capr.content)
            f.close()

        captcha = Image.open('C:\\Users\\taoju\\Desktop\\captcha_newmember.png')
        captcha.show()
        signup_captcha = raw_input("Please input the captcha：")
        #print signup_captcha
        self.captcha = signup_captcha

    def _newmember(self):

        id = raw_input("Please input the ID：")
        viewstate = raw_input("Please input the VIEWSTATE：")
        eventvalidation = raw_input("Please input the EVENTVALIDATION：")
        uniqueId = raw_input("Please input the UniqueId：")
        captchaControl = raw_input("Please input the CaptchaControl：")

        newmember_url = 'https://aaa.pinnaclesports.com/Members/NewMember.aspx'

        newmember_header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                  'Cache-Control':'max-age=0',
                  'Connection':'keep-alive',
                  'Content-Type':'application/x-www-form-urlencoded',
                  'DNT':'1',
                  'Host':'aaa.pinnaclesports.com',
                  'Origin':'https://aaa.pinnaclesports.com',
                  'Referer':'https://aaa.pinnaclesports.com/Members/NewMember.aspx',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}


        postData = {'__LASTFOCUS':'',
            '__EVENTTARGET':'',
            '__EVENTARGUMENT':'',
            '__VIEWSTATE':viewstate,
            '__VIEWSTATEGENERATOR':'2B21570D',
            '__EVENTVALIDATION':eventvalidation,
            'ctl00$PCPH$UniqueId':uniqueId,
            'ctl00$PCPH$AL1DDL':'0',
            'ctl00$PCPH$AL2DDL':'0',
            'ctl00$PCPH$AL3DDL':id,
            'ctl00$PCPH$PTB':self.password,
            'ctl00$PCPH$FNTB':'Tt',
            'ctl00$PCPH$LNTB':'',
            'ctl00$PCPH$PHTB':'',
            'ctl00$PCPH$MTB':'',
            'ctl00$PCPH$MCTB':'1000',
            'ctl00$PCPH$OTDDL':'HongKong',
            'ctl00$PCPH$CDDL':'Hong Kong',
            'ctl00$PCPH$COTB':'',
            'ctl00_PCPH_GroupCommissionsPopupCtrl_ComPopupControlWS':'0:0:-1:-10000:-10000:0:1000px:400px:1:0:0:0',
            'ctl00$PCPH$SSPTDL$ctl00$SSPTH2H':'Soccer',
            'ctl00$PCPH$SSPTDL$ctl00$SSSportSubTypeH':'Eng. Premier',
            'ctl00$PCPH$SSPTDL$ctl00$SSPT2TB':'',
            'ctl00$PCPH$SSPTDL$ctl00$SSPT4TB':'',
            'ctl00$PCPH$SSPTDL$ctl00$SSPT6TB':'',
            'ctl00$PCPH$CustomerWagerMaxSelectionCtrl$DDWagerMaximumSelection':'1',
            'ctl00$PCPH$CaptchaControl$InputTB':self.captcha,
            'ctl00$PCPH$CaptchaControl$cc':captchaControl,
            'ctl00$PCPH$CRB':'Create',
            'DXScript':'1_157,1_89,1_149,1_100,1_86,1_141,1_139',
            'DXCss':'100_95,1_9,1_11,1_4,100_97,100_241,100_243,/Members/Agent.css,/css/MembersAsianAgentAdminMaster?v=tu_PZM2apLZcVD3qdoCl-sSqyNjWxnJjSUFqvHE5ITQ1'}

        req = pinnacle_session.post(newmember_url, postData,headers=newmember_header,timeout=60*20)
        try:
            content = str(req.content)
            print content
        except  urllib2.HTTPError, e:
            print e.code

    def login(self):

        self._loginmain()
        self._kickoff()
        #self._parserpage()
        #self._savedata()
        self._getcaptcha()
        self._newmember()

if __name__ == '__main__':

    userlogin = PinnacleLogin()
    username = ''
    password = ''

    userlogin.set_login_info(username,password)
    userlogin.login()
    pinnacle_session.close()



