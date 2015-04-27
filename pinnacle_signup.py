# -*- coding: utf-8 -*-
import urllib2
import urllib
#from pytesser import *
import requests
import cookielib
import sys
from PIL import Image
import bs4
import re
import os

######
reload(sys)
sys.setdefaultencoding("utf8")
######
signup_url = 'https://www.pinnaclesports.com/signup/desktop/en-GB#signup_homepage'
post_url = 'https://www.pinnaclesports.com/signup/ValidateRequest/Desktop/en-GB?Length=7'
signup_session = requests.Session()

class PinnacleSignUp():
    """Automatically signup the Pinnacle"""
    def __init__(self):

        self.firstname = ''
        self.surename = ''
        self.password = ''
        self.email = ''
        #self.cookie = ''
        self.captcha = ''
        self.captcha_url = ''

        #self.cj = cookielib.CookieJar()
        #self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj),urllib2.HTTPHandler)
        #urllib2.install_opener(self.opener)


    def set_signup_info(self,firstname,surename,password,email):
        '''set the user information'''
        self.firstname = firstname
        self.surename = surename
        self.password = password
        self.email = email

    def _sigupmain(self):
        '''Sign up'''
        request_header = headers = {'Accept':'*/*',
                                    #'Accept-Encoding':'gzip, deflate',
                                    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                                    'Connection':'keep-alive',
                                    #'Content-Length':'361',
                                    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                                    #'Cookie':self.cookie,
                                    'DNT':'1',
                                    'Host':'www.pinnaclesports.com',
                                    'Origin':'https://www.pinnaclesports.com',
                                    'Referer:https':'//www.pinnaclesports.com/signup/desktop/en-GB',
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
                                    'X-Requested-With':'XMLHttpRequest'}

        postData = {
            'FirstName':self.firstname,
            'LastName':self.surename,
            'Email':self.email,
            'ConfirmEmail':self.email,
            'DateOfBirthDay':8,
            'DateOfBirthMonth':8,
            'DateOfBirthYear':1988,
            'CountryCode':'HKG',
            'Address1':'abc',
            'Address2':'',
            'City':'abc',
            'RegionId':'',
            'PostalCode':52888,
            'Telephone':123456789098,
            'CurrencyCode':'HKD',
            'Password':self.password,
            'ConfirmPassword':self.password,
            'SecurityQuestion':'mm',
            'SecurityAnswer':'mm',
            'TypeInNumbers':self.captcha,
            'SubscribeToMarketing':'False',
            'HowDidYouHear':'',
            'AgreeTermsOfService':'true',
            'AgreeTermsOfService':'true',
            'X-Requested-With':'XMLHttpRequest'}


        req = signup_session.post(post_url, postData,headers=request_header,timeout=60*4)
        content = str(req.content)
        #print content
        tag = 'Thank you for opening an account with Pinnacle Sports'
        if  re.search(tag,content):
            #signup successful
            print tag
        else:
            #signup failure
            print 'Sign up failure\n'

    def _getcaptcha(self):
        capr = signup_session.get(self.captcha_url,timeout=60*4)
        with open('C:\\captcha.png', 'wb') as f:
            f.write(capr.content)
            f.close()
        signup_captcha = raw_input("Please input the captcha：")
        print signup_captcha
        self.captcha = signup_captcha

    def _setcookies(self):

        getCode = signup_session.get(signup_url,timeout=60*4)
        #print getCode.text
        signup_cookie = (signup_session.cookies.values()[1])[3:]
        #print signup_cookie
        #signup_cookie = raw_input("请输入cookies：")
        #print signup_cookie
        self.captcha_url = 'https://www.pinnaclesports.com/signup/Desktop/c?sid='+signup_cookie
        #self.cookie = 'PCTR=637222036955717448; vidi=9bff34a3a2cd4069bba9ee1a3f1cc63a; ASP.NET_SessionId=ohzzyg0bb32c45yvuk4xu5vx; LastPageCookie=url=http://www.pinnaclesports.com/default.aspx&time=25/04/2015 15:33:59; UserPrefsCookie=device=d&languageGroup=all&languageId=2&linesTypeView=c&priceStyle=decimal;ADRUM_BT=R%3a0%7cclientRequestGUID%3a88f2cece-0147-48d0-bca7-f6a7ffbbac1f%7cbtId%3a1117; signup_sd='+signup_cookie+',cps:3mQAuFP+Jhpo+24xnX+5xA=='
        #self.cookie_get = 'UserPrefsCookie=device=d&languageGroup=all&languageId=2&linesTypeView=c&priceStyle=decimal; signup_sd=id:'+signup_cookie+',cps:hpGaScgtf9sA3+PplTiAwQ=='


    def signup(self):

        self._setcookies()
        self._getcaptcha()
        self._sigupmain()


if __name__ == '__main__':

    usersignup = PinnacleSignUp()
    firstname = 'TTTTT'
    surename = 'ccc'
    password = 'qqqq212$'
    email = 'taojun.li@outlook.com'

    usersignup.set_signup_info(firstname,surename,password,email)
    usersignup.signup()
