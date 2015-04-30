# -*- coding: utf-8 -*-
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

pinnacle_session = requests.Session()#create a session

class PinnacleMember():
    '''new member data'''

    def _init_(self):

        #for creating a new Member
        self.customer_id = '' #new member name: delegate name+member id
        self.id_first = ''
        self.id_second = ''
        self.id_third = ''
        self.password_init = ''
        self.password_new = ''
        self.lastname = ''
        self.firstname = ''
        self.credit_limit = ''

    def setMemberInitPassword(self,password_init):
        self.password_init = password_init

    def setMemberNewPassowrd(self,password_new):
        self.password_new = password_new

    def setMemberName(self,firstname,lastname):
        self.firstname = firstname
        self.lastname = lastname

    def setMemberId(self,first,second,third):
        self.id_first = first
        self.id_second = second
        self.id_third = third

    def setCreditLimit(self,credit_limit):
        self.credit_limit = credit_limit


class PinnacleLogin(PinnacleMember):
    """Automatically login the Pinnacle.com to get the data of Balance Sheet"""

    def __init__(self):

        self.username = ''
        self.password = ''
        self.pinnacle_balance = ''
        self.balance_sheet = {} #result saved in this table

        #items to post for new member, finding out in the new member page
        self.captcha_url = ''
        self.captcha = ''
        self.captcha_control = ''
        self.unique_id = ''
        self.view_state = ''
        self.event_validation = ''

    def setlogin_info(self,username,password):
        '''set the user information'''
        self.username = username
        self.password = self.password_init = password

    def _loginmain(self):
        '''login the background main page'''
        login_url = 'https://aaa.pinnaclesports.com/Login.aspx'

        login_header ={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
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

        login_postData = {'__VIEWSTATE':'/wEPDwUINDc3MzExNzIPZBYCAgMPZBYCAgEPZBYCAgMPEGQPFgECBxYBEAUEVGhhaQUCdGhnFgFmZGRevYPRLil7tSWwrGv94kOQWgS/Z/UdYWX+2Psw3JdwrQ==',
            '__VIEWSTATEGENERATOR':'C2EE9ABB',
            '__EVENTVALIDATION':'/wEdAA0XhIbGiuWL6wNXsuKKNl9+zyjSCk071VEBFi+Pn+x7Vbskj2bYtjy6x+ok0AhsxbmaWJgNYxXDKJmfHo3SUAtyDajVEjtqqAB+Fe3DJW2ReMqDhLSZLEX/ZvMqb4F5bexjIsOsOCcsfe6l6fcRigHQEAWAfkf0gHlvWmxI/1mZHAgsYlVDpoodEWRg9RRToQqwRQmdYVIGdQOw5ctONxUqR1LBKX1P1xh290RQyTesRVwK8/1gnn25OldlRNyIednDbiWC8p5oWQ9KZC32jRIUQPgwUS8va+KcSB9QJ0dkZouFlD3gerUhEyV9P/WYD/o=',
            'UPBF$LDDL':'en-GB',
            'UserName': self.username,
            'Password': self.password,
            'LB':'Login'}

        req = pinnacle_session.post(login_url, login_postData,headers=login_header,timeout=60*4)


    def _kickoff(self):
        '''kick off other user and continue'''
        login_header ={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
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


        kickoff_url = 'https://aaa.pinnaclesports.com/AlreadyLoggedIn.aspx'

        postData = {'__VIEWSTATE':'/wEPDwULLTEzMDIzODIwMTNkZOmQJfUJyJT5fL5xtNAp2w1JEhyndb8AJjxA3GoJBox8',
        '__VIEWSTATEGENERATOR':'9461229B',
        '__EVENTVALIDATION':'/wEdAAXI5Cf5IjAXLSFBNsvmq/sRUbCimvzN/TczT4kz9qKpYnFNg25++/wnLLvx/zMOPgtg4wULag6puEpGFyFXlupb70/AcP6TbUveJn5MuDyMx7c9aL0zH/wbg+CtvVsRp1Fi1jTGdqVURYr7DEN6f2Fe',
        'LIHF': self.username,
        'LPHF': self.password,
        'COB':'Continue'}

        req = pinnacle_session.post(kickoff_url, postData,headers=login_header,timeout=60*4)
        self.pinnacle_balance = str(req.content)


        tag = 'Yesterday Total Balance'
        if  re.search(tag,self.pinnacle_balance):
            #login successful
            print 'Login successful!\n'
        else:
            #login failure
            print 'Login failed, please check the result.html file for details\n'

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
        sName = os.path()+'pinnacle_balance' + '.txt'
        try:
            f = open(sName,'w')
            for (k,v) in self.balance_sheet.items():
                f.write("%s: %s\n" % (k,v))
            f.close()
            print 'balance_sheet saved in the dictionary ' + sName + '......'
        except IOError:
            print "Cannot create the file!"


    def _getpagedata(self):
        """get the post data and captcha url from the new member page"""

        url = 'https://aaa.pinnaclesports.com/Members/NewMember.aspx'
        getCode = pinnacle_session.get(url,timeout=60*4)
        str = getCode.content

        #get the captcha_url
        captcha_url_post = re.findall("CaptchaHandler\.ashx\?cc=(.*)\"",str)
        self.captcha_control = captcha_url_post[0]
        self.captcha_url = 'https://aaa.pinnaclesports.com/UserControls/CaptchaApp/CaptchaHandler.ashx?cc='+captcha_url_post[0]

        #get the uniqueid for postdata
        UniqueId = re.findall("ctl00\_PCPH\_UniqueId\"\svalue\=\"(.*)\"",str)
        self.unique_id = UniqueId[0]

        #get the VIEWSTATE for postdata
        VIEWSTATE = re.findall("\_\_VIEWSTATE\"\svalue\=\"(.*)\"",str)
        self.view_state = VIEWSTATE[0]

        #get the EVENTVALIDATION for postdata
        EVENTVALIDATION = re.findall("\_\_EVENTVALIDATION\"\svalue\=\"(.*)\"",str)
        self.event_validation = EVENTVALIDATION[0]


    def _getcaptcha(self):
        '''automatically download and open the captcha picture for recognization'''

        self._getpagedata()

        captcha_path = os.getcwd()+'\\captcha_newmember.png'
        capr = pinnacle_session.get(self.captcha_url,timeout=60*4)
        with open(captcha_path, 'wb') as f:
            f.write(capr.content)
            f.close()

        captcha = Image.open(captcha_path)
        captcha.show() #open the captcha image
        signup_captcha = raw_input("Please input the captcha：")
        self.captcha = signup_captcha


    def _newmember(self):
        '''Create a new member under the delegate user'''

        newmember_url="https://aaa.pinnaclesports.com/Members/NewMember.aspx"

        newmember_header = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                  "Accept-Encoding":"gzip, deflate",
                  "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
                  "Cache-Control":"max-age=0",
                  "Connection":"keep-alive",
                  "Content-Type":"application/x-www-form-urlencoded",
                  "DNT":"1",
                  "Host":"aaa.pinnaclesports.com",
                  "Origin":"https://aaa.pinnaclesports.com",
                  "Referer":"https://aaa.pinnaclesports.com/Members/NewMember.aspx",
                  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}

        postData = {"__EVENTTARGET":"",
                    "__EVENTARGUMENT":"",
                    "__VIEWSTATE":self.view_state,
                    "__VIEWSTATEGENERATOR":"2B21570D",
                    "__EVENTVALIDATION":self.event_validation,
                    "ctl00$PCPH$UniqueId":self.unique_id,
                    "ctl00$PCPH$AL1DDL":self.id_first, #id,first
                    "ctl00$PCPH$AL2DDL":self.id_second,
                    "ctl00$PCPH$AL3DDL":self.id_third,
                    "ctl00$PCPH$PTB":self.password_init,
                    "ctl00$PCPH$FNTB":self.firstname,
                    "ctl00$PCPH$LNTB":self.lastname,
                    "ctl00$PCPH$PHTB":"",
                    "ctl00$PCPH$MTB":"",
                    "ctl00$PCPH$MCTB":self.credit_limit,
                    "ctl00$PCPH$OTDDL":"HongKong",
                    "ctl00$PCPH$CDDL":"Hong Kong",
                    "ctl00$PCPH$COTB":"",
                    "ctl00_PCPH_GroupCommissionsPopupCtrl_ComPopupControlWS":"0:0:-1:-10000:-10000:0:1000px:400px:1:0:0:0",
                    "ctl00$PCPH$SSPTDL$ctl00$SSPTH2H":"Soccer",
                    "ctl00$PCPH$SSPTDL$ctl00$SSSportSubTypeH":"Eng. Premier",
                    "ctl00$PCPH$SSPTDL$ctl00$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl00$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl00$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl00$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl00$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl00$SSPT16DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl00$SSPT17DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl00$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl00$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl00$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl01$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl01$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl01$SSPT16DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl01$SSPT17DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl01$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl01$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl01$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl01$LiveCopyFromDeadbHidden":"false",
                    "ctl00$PCPH$SSPTDL$ctl02$SSSportSubTypeH":"Bundesliga",
                    "ctl00$PCPH$SSPTDL$ctl02$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl02$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl02$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl02$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl02$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl02$SSPT16DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl02$SSPT17DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl02$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl02$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl02$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl03$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl03$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl03$SSPT16DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl03$SSPT17DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl03$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl03$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl03$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl03$LiveCopyFromDeadbHidden":"false",
                    "ctl00$PCPH$SSPTDL$ctl04$SSSportSubTypeH":"Serie A",
                    "ctl00$PCPH$SSPTDL$ctl04$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl04$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl04$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl04$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl04$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl04$SSPT16DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl04$SSPT17DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl04$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl04$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl04$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl05$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl05$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl05$SSPT16DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl05$SSPT17DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl05$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl05$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl05$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl05$LiveCopyFromDeadbHidden":"false",
                    "ctl00$PCPH$SSPTDL$ctl06$SSSportSubTypeH":"La Liga",
                    "ctl00$PCPH$SSPTDL$ctl06$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl06$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl06$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl06$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl06$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl06$SSPT16DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl06$SSPT17DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl06$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl06$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl06$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl07$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl07$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl07$SSPT16DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl07$SSPT17DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl07$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl07$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl07$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl07$LiveCopyFromDeadbHidden":"false",
                    "ctl00$PCPH$SSPTDL$ctl08$SSSportSubTypeH":".",
                    "ctl00$PCPH$SSPTDL$ctl08$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl08$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl08$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl08$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl08$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl08$SSPT16DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl08$SSPT17DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl08$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl08$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl08$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl09$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl09$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl09$SSPT16DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl09$SSPT17DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl09$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl09$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl09$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl09$LiveCopyFromDeadbHidden":"false",
                    "ctl00$PCPH$SSPTDL$ctl10$SSPTH2H":"Basketball",
                    "ctl00$PCPH$SSPTDL$ctl10$SSSportSubTypeH":"NBA",
                    "ctl00$PCPH$SSPTDL$ctl10$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl10$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl10$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl10$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl10$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl10$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl10$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl10$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl11$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl11$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl11$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl11$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl11$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl11$LiveCopyFromDeadbHidden":"false",
                    "ctl00$PCPH$SSPTDL$ctl12$SSSportSubTypeH":"NCAA",
                    "ctl00$PCPH$SSPTDL$ctl12$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl12$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl12$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl12$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl12$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl12$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl12$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl12$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl13$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl13$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl13$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl13$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl13$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl13$LiveCopyFromDeadbHidden":"false",
                    "ctl00$PCPH$SSPTDL$ctl14$SSSportSubTypeH":".",
                    "ctl00$PCPH$SSPTDL$ctl14$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl14$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl14$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl14$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl14$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl14$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl14$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl14$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl15$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl15$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl15$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl15$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl15$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl15$LiveCopyFromDeadbHidden":"false",
                    "ctl00$PCPH$SSPTDL$ctl16$SSPTH2H":"Football",
                    "ctl00$PCPH$SSPTDL$ctl16$SSSportSubTypeH":"NCAA",
                    "ctl00$PCPH$SSPTDL$ctl16$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl16$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl16$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl16$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl16$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl16$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl16$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl16$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl17$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl17$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl17$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl17$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl17$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl17$LiveCopyFromDeadbHidden":"false",
                    "ctl00$PCPH$SSPTDL$ctl18$SSSportSubTypeH":"NFL",
                    "ctl00$PCPH$SSPTDL$ctl18$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl18$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl18$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl18$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl18$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl18$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl18$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl18$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl19$SSSportSubTypeH":".",
                    "ctl00$PCPH$SSPTDL$ctl19$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl19$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl19$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl19$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl19$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl19$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl19$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl19$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl20$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl20$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl20$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl20$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl20$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl20$LiveCopyFromDeadbHidden":"false",
                    "ctl00$PCPH$SSPTDL$ctl21$SSPTH2H":"Baseball",
                    "ctl00$PCPH$SSPTDL$ctl21$SSSportSubTypeH":"MLB",
                    "ctl00$PCPH$SSPTDL$ctl21$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl21$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl21$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl21$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl21$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl21$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl21$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl21$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl22$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl22$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl22$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl22$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl22$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl22$LiveCopyFromDeadbHidden":"false",
                    "ctl00$PCPH$SSPTDL$ctl23$SSSportSubTypeH":".",
                    "ctl00$PCPH$SSPTDL$ctl23$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl23$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl23$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl23$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl23$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl23$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl23$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl23$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl24$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl24$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl24$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl24$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl24$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl24$LiveCopyFromDeadbHidden":"false",
                    "ctl00$PCPH$SSPTDL$ctl25$SSPTH2H":"Hockey",
                    "ctl00$PCPH$SSPTDL$ctl25$SSSportSubTypeH":"NHL OT Incl",
                    "ctl00$PCPH$SSPTDL$ctl25$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl25$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl25$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl25$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl25$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl25$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl25$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl25$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl26$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl26$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl26$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl26$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl26$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl26$LiveCopyFromDeadbHidden":"false",
                    "ctl00$PCPH$SSPTDL$ctl27$SSSportSubTypeH":"NHL Reg Time",
                    "ctl00$PCPH$SSPTDL$ctl27$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl27$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl27$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl27$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl27$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl27$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl27$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl27$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl28$SSSportSubTypeH":".",
                    "ctl00$PCPH$SSPTDL$ctl28$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl28$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl28$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl28$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl28$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl28$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl28$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl28$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl29$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl29$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl29$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl29$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl29$SSPTC3HF":"false",
                    "ctl00$PCPH$SSPTDL$ctl29$LiveCopyFromDeadbHidden":"false",
                    "ctl00$PCPH$SSPTDL$ctl30$SSPTH2H":"All Other Sports",
                    "ctl00$PCPH$SSPTDL$ctl30$SSSportSubTypeH":".",
                    "ctl00$PCPH$SSPTDL$ctl30$SSPT2TB":"",
                    "ctl00$PCPH$SSPTDL$ctl30$SSPT4TB":"",
                    "ctl00$PCPH$SSPTDL$ctl30$SSPT6TB":"",
                    "ctl00$PCPH$SSPTDL$ctl30$SSPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl30$SSPT15DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl30$SSPT18DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl30$SSPT19DDL":"0.00",
                    "ctl00$PCPH$SSPTDL$ctl30$SSPTC3HF":"false",
                    "ctl00$PCPH$SIPT2TB":"",
                    "ctl00$PCPH$SIPT4TB":"",
                    "ctl00$PCPH$SIPT14DDL$HoldDropDownList":"0.00",
                    "ctl00$PCPH$SIPT15DDL":"0.00",
                    "ctl00$PCPH$SIPT16DDL":"0.00",
                    "ctl00$PCPH$SIPT51DDL":"0.00",
                    "ctl00$PCPH$SIPTC3HF":"false",
                    "ctl00$PCPH$CustomerWagerMaxSelectionCtrl$DDWagerMaximumSelection":"1",
                    "ctl00$PCPH$CaptchaControl$InputTB":self.captcha,
                    "ctl00$PCPH$CaptchaControl$cc":self.captcha_control,
                    "ctl00$PCPH$CRB":"Create",
                    "DXScript":"1_157,1_89,1_149,1_100,1_86,1_141,1_139",
                    "DXCss":"100_95,1_9,1_11,1_4,100_97,100_241,100_243,/Members/Agent.css,/css/MembersAsianAgentAdminMaster?v=tu_PZM2apLZcVD3qdoCl-sSqyNjWxnJjSUFqvHE5ITQ1"}

        req = pinnacle_session.post(newmember_url, postData,headers=newmember_header,timeout=60*4)

        str = req.content
        tag = 'Last Login IP'
        if  re.search(tag,str):
            #signup successful
            print 'Create a new Member!\n'

        else:
            #signup failure
            print 'Can not create a new Member!\n'

        pinnacle_session.close()


    def _resetpassword(self):
        '''login from the homepage with the new member id, then change the password'''

        reset_session = requests.Session() #create a session

        cookie_init = 'PCTR=637235794190443421; UserAccess=2; GRP=!QT9dcstfHn7HSpguFjtGspOx3359jiDO60X9GcYCLM3Sud0cVcW5WsE=; bootstraprun=no; PinMemCookie=h=687ABFEDF48066AE68529B112EB39D44&v=members.pinnaclesports.com&t=ps-mc; ASP.NET_SessionId=nmdei410wv1x3gdhopa2vuqk; UserPrefsCookie=languageId=2&priceStyle=decimal&linesTypeView=c&device=d&languageGroup=all; LastPageCookie=url=http://www.pinnaclesports.com/default.aspx&time=30/04/2015 15:24:53'

        login_url = 'https://www.pinnaclesports.com/login/authenticate/Classic/en-GB'

        login_header ={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                  'Cache-Control':'max-age=0',
                  'Connection':'keep-alive',
                  'Cookie':cookie_init,
                  'Content-Type':'application/x-www-form-urlencoded',
                  'DNT':'1',
                  'Host':'www.pinnaclesports.com',
                  'Origin':'https://www.pinnaclesports.com',
                  'Referer':'https://www.pinnaclesports.com/',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

        self.customer_id = self.username+str(self.id_first)+str(self.id_second)+str(self.id_third)

        login_postData = {'ctl00$LDDL':'2',
                    'ctl00$PSDDL':'decimal',
                    'CustomerId':self.customer_id,
                    'Password':self.password_init,
                    'AppId':'Classic'}

        req = reset_session.post(login_url, login_postData,headers=login_header,timeout=60*4)

        cookies ='PCTR=637235794190443421; ASP.NET_SessionId=5krztnl4wrzkr5na0art0pfq; signup_sd=id:656ea2dc-22d9-4eb1-8b17-43fba9091fc2,cps:xJNTKAjYrwePbZcLo2rQAw==; enhanced=pass; LastPageCookie=url=http://www.pinnaclesports.com/default.aspx&time=29/04/2015 17:02:38; '
        cookies = cookies+'custid='+reset_session.cookies['custid']+'; '+'UserPrefsCookie='+reset_session.cookies['UserPrefsCookie']+'; '+'UserAccess='+reset_session.cookies['UserAccess']+'; '+'GRP='+reset_session.cookies['GRP']+'; '+'bootstraprun='+reset_session.cookies['bootstraprun']+'; '+'PinMemCookie='+reset_session.cookies['PinMemCookie']+'; '+'ADRUM_BT='+reset_session.cookies['ADRUM_BT']


        tag = 'Login unsuccessful'
        if  re.search(tag,req.content):
            #login successful
            print 'Login unsuccessful!\n'
        else:
            pass

        #commit and next step
        changepwd_url = 'https://www.pinnaclesports.com/login/password/ResetConfirmation/Classic/en-GB'

        changepwd_header ={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                  'Connection':'keep-alive',
                  'Cookie':cookies,
                  'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                  'DNT':'1',
                  'Host':'www.pinnaclesports.com',
                  'Origin':'https://www.pinnaclesports.com',
                  'Referer':'https://www.pinnaclesports.com/login/password/ResetConfirmation/Classic/en-GB',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
                  'X-Requested-With':'XMLHttpRequest'}


        change_postData = {'NextSteps':'',
                              'CurrentPassword':self.password_init,
                              'NewPassword':self.password_new,
                              'ConfirmPassword':self.password_new}

        req = reset_session.post(changepwd_url, change_postData,headers=changepwd_header,timeout=60*4)

        tag = 'Saved successfully'
        if  re.search(tag,req.content):
            print 'Change password successful!\n'+'You have created a new Member: '+self.customer_id+', Credit Limit: '+str(self.credit_limit)
            pass
        else:
            print 'Reset Password unsuccessful!\n'

        #continue and last step
        changepwd_url = changepwd_url+'?customerId='+self.customer_id+'&nextSteps=5&IsAjaxRequest=True'
        req = reset_session.get(changepwd_url)

        tag = 'Reset Password'
        if  re.search(tag,req.content):
            pass
        else:
            print 'Change password failed\n'


    def login(self):

        self._loginmain()
        self._kickoff()
        #self._parserpage()# parser the member list page
        #self._savedata() # save the member list
        self._getcaptcha()
        self._newmember()
        self._resetpassword()# reset the password


if __name__ == '__main__':

    userlogin = PinnacleLogin()
    delegate_username = ''
    delegate_password = ''

    userlogin.setlogin_info(delegate_username,delegate_password) # background login
    userlogin.setMemberId(0,0,'F')#set the last three numbers or alphabets of the memberID
    userlogin.setCreditLimit(0) #set the credit limit
    userlogin.setMemberName('T','Test')#set the firstname and lastname
    userlogin.setMemberNewPassowrd('')#set the new password

    userlogin.login()


