# -*- coding: utf-8 -*-
import sys
import re
import requests
import os
import time
import datetime
######
reload(sys)
######
login_url = 'https://aaa.pinnaclesports.com/Login.aspx'
login_session = requests.Session()
log_path = sys.path[0]+'\\logs\\'

class Pinnacle():
    """Automatically login the Pinnacle to get the data of Balance Sheet"""
    def __init__(self,refresh=30):

        self.username = ''
        self.password = ''
        self.isLogin = False
        self.refreshTime = refresh

    def setInfo(self,username,password):
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
        try:
            req = login_session.post(login_url, postData,headers=login_header)

        except Exception, e:
            print 'login fail: ', e
            return False

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
        try:

            req = login_session.post(kickoff_url, postData,headers=login_header)
            self.pinnacle_balance = str(req.content)

            tag = 'Yesterday Total Balance'
            if  re.search(tag,self.pinnacle_balance):
                #login successful
                self.isLogin = True
                print 'login successful!\n'
                return True
            else:
                #login failure
                print 'login failure!\n'
                return False

            #req.close()
        except Exception, e:
            print 'login fail: ', e
            return False

    def _findticket(self,ticket):

        header = {'Content-Type':'application/x-www-form-urlencoded',
                  'Host':'aaa.pinnaclesports.com',
                  'Origin':'https://aaa.pinnaclesports.com',
                  'Referer':'https://aaa.pinnaclesports.com/FindTicket/FindTicket',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}


        findticket_url = 'https://aaa.pinnaclesports.com/AlreadyLoggedIn.aspx'

        postData = {'__VIEWSTATE':'/wEPDwULLTEzMDIzODIwMTNkZA==',
                    'txtTicketNo':ticket,
                    'LDDL':'en-GB',
                    '__VIEWSTATEGENERATOR':'9461229B'}

        try:
            req = login_session.post(findticket_url, postData,headers=header)

            ticketinfo_url='https://aaa.pinnaclesports.com/Wagers/SearchTicket/'+str(ticket)
            ticketinfo = login_session.get(ticketinfo_url)
            #print str(ticketinfo.content)
            tagIsTicket='Trans\.'
            tagHasNo = 'No data to display'
            tagReject ='Rejected'
            isticket=re.findall(tagIsTicket,ticketinfo.content)
            if isticket:
                hasNo=re.findall(tagHasNo,ticketinfo.content)
                hasRejected=re.findall(tagReject,ticketinfo.content)
                if hasNo:
                      print 'no ticket'
                      return 2
                else:
                    if hasRejected:
                        print str(ticket)+' has been rejected!'
                        return 3
                    else:
                        print str(ticket)+' is successful!'
                        return 1
            else:
                print 'not Pinnacle\'s ticket'
                return 4
        except Exception, e:
            print e
            return False

    def _logcheck(self,logname):

        ACCOUNT_PINNACLE= '\xd5\xcb\xbb\xa7:Pinnacle' #account line[5]
        STATUS_SUCCESS ='\xd7\xb4\xcc\xac:Success'  #status line[4]
        STATUS_WAITING ='\xd7\xb4\xcc\xac:Waiting'  #status line[4]
        STATUS_REJECT ='\xd7\xb4\xcc\xac:\xd7\xa2\xd2\xe2\xb4\xcb\xb5\xa5\xb1\xbb\xbb\xae' #请注意！此单被划！
        TICKET = '\xb5\xa5\xba\xc5:' #ticket id line[3]
        #self.login_name = '' #line[6]

        logfile=log_path+logname+'.log'
       #newlogfile = re.findall(r'(.*)\.log',logname)[0]+'m.log'
        newlogfile =logname+'m.log'
        newlog = log_path+str(newlogfile)

        if self.isLogin is True:
            try:
                if os.path.isfile(newlog):
                    os.remove(newlog)
                log=open(logfile,'r')
                lines =  log.readlines()
                for line in lines:
                    line = line.split()
                    if ACCOUNT_PINNACLE in line:
                        if STATUS_WAITING in line:
                            ticket = re.findall("\xb5\xa5\xba\xc5:(.*)",line[3])[0] #paser ticket
                            #print line[3]+' '+line[4]+' '+line[6]+' '+str(self.ticket)
                            checkT=self._findticket(ticket)
                            if checkT == 1:
                                line[4]=line[4].replace(STATUS_WAITING,STATUS_SUCCESS)
                            elif checkT == 3:
                                line[4]=line[4].replace(STATUS_WAITING,STATUS_REJECT)
                            else:
                                pass
                    line.append('\n')
                    line='\t'.join(line)
                    open(newlog,'a+').writelines(line)

                log.close()
                return True

            except IOError:
                print('File Error!')
            finally:
                log.close()

    def _loglist(self):

        loglist=[]
        for logs in os.listdir(log_path):
             loglist.append(logs)
        return loglist

    def logModify(self):

        self._loginmain()
        r=self._kickoff()

        #loglist=self._loglist()
        data = datetime.date.today().strftime("%Y-%m-%d")
        log = data
        if r:
            try:
                #for log in loglist:
                    #if 'm' not in log:
                print 'modifying:'+log
                self._logcheck(log)
                return True
            except:
                return False

    def logRefresh(self):
        while True:
            r=self.logModify()
            if not r:
                print 'log Modify fail!'
            time.sleep(self.refreshTime)


if __name__ == '__main__':

    pinnacle = Pinnacle()
    username = ''
    password = ''

    pinnacle.setInfo(username,password)
    pinnacle.logRefresh()
