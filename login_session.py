# -*- coding: utf-8 -*-
#import urllib2
#import urllib
#import cookielib
import sys
import bs4
import re
import requests
import os

######
reload(sys)
sys.setdefaultencoding("utf8")
######
login_url = 'https://aaa.pinnaclesports.com/Login.aspx'
login_session = requests.Session()

class PinnacleLogin():
    """Automatically login the Pinnacle to get the data of Balance Sheet"""
    def __init__(self):

        self.username = ''
        self.password = ''
        self.pinnacle_balance = ''
        self.balance_sheet = {} #result saved in this table

    def set_login_info(self,username,password):
        '''set the user information'''
        self.username = username
        self.password = password

    def _loginmain(self):
        '''login the main page'''

        login_header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
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


        postData = {'__VIEWSTATE':'/wEPDwUINDc3MzExNzIPZBYCAgMPZBYCAgEPZBYCAgMPEGQPFgECBxYBEAUEVGhhaQUCdGhnFgFmZGRevYPRLil7tSWwrGv94kOQWgS/Z/UdYWX+2Psw3JdwrQ==',
            '__VIEWSTATEGENERATOR':'C2EE9ABB',
            '__EVENTVALIDATION':'/wEdAA0XhIbGiuWL6wNXsuKKNl9+zyjSCk071VEBFi+Pn+x7Vbskj2bYtjy6x+ok0AhsxbmaWJgNYxXDKJmfHo3SUAtyDajVEjtqqAB+Fe3DJW2ReMqDhLSZLEX/ZvMqb4F5bexjIsOsOCcsfe6l6fcRigHQEAWAfkf0gHlvWmxI/1mZHAgsYlVDpoodEWRg9RRToQqwRQmdYVIGdQOw5ctONxUqR1LBKX1P1xh290RQyTesRVwK8/1gnn25OldlRNyIednDbiWC8p5oWQ9KZC32jRIUQPgwUS8va+KcSB9QJ0dkZouFlD3gerUhEyV9P/WYD/o=',
            'UPBF$LDDL':'en-GB',
            'UserName': self.username,
            'Password': self.password,
            'LB':'Login'}

        req = login_session.post(login_url, postData,headers=login_header,timeout=60*4)


    def _kickoff(self):
        '''kick off other user and continue'''

        login_header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
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

        req = login_session.post(kickoff_url, postData,headers=login_header,timeout=60*4)
        self.pinnacle_balance = str(req.content)

        tag = 'Yesterday Total Balance'
        if  re.search(tag,self.pinnacle_balance):
            #login successful
            print 'Logged in successfully!\n'
        else:
            #login failure
            print 'Logged in failed, check result.html file for details\n'

        req.close()

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

    def login(self):

        self._loginmain()
        self._kickoff()
        self._parserpage()
        #self._savedata()


if __name__ == '__main__':

    userlogin = PinnacleLogin()
    username = ''
    password = ''

    userlogin.set_login_info(username,password)
    userlogin.login()




