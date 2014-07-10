#!/usr/local/bin/python
#coding=utf-8
# -------------------------------------------------------------------------------
#每隔10秒ping一次服务器，累计三次和累计十次不通则发邮件提醒
#
# -------------------------------------------------------------------------------
import pexpect
import time
import smtplib
from email.mime.text import MIMEText
import ConfigParser
import string, os ,sys


#### 配置服务器IP地址
check_ip ={"100.0.0.86":0,"100.0.0.249":0,}
#### 定义几次ping不通发邮件
send_mail_limit = [3,10] 

class InitSetting(file_name):
    '''
    初始化本地设置
    '''
    def __init__(self,file_name):
        self.file_name = file_name
        self.cf = None
        cf = ConfigParser.ConfigParser()
        self._mail_host = " "
        self._mail_user = " "
        self._mail_pwd =  " "
        self._mail_to = " "
        self._mail_cc = " "
        


    def loading_ini(self):
        if not cf:
            cf = ConfigParser.ConfigParser()
        cf.read(self.file_name)
        self._mail_host = cf.get("mail","mail_host")
        self._mail_user = cf.get("mail","mail_user")
        self._mail_pwd = cf.get("mail","mail_pwd")
        self._mail_to = cf.get("mail","mail_to")
        self._mail_cc = cf.get("mail","mail_cc")


    def mail_host(self):
        return self._mail_host

    def mail_user(self):
        return self._mail_user

    def mail_pwd(self):
        return self._mail_pwd

    def mail_to(self):
        return self._mail_to

    def mail_cc(self):
        return self._mail_cc
 
def mail_warn(error_ip,mail_address):
    '''
    发送模块
    '''
    content = 'Ping IP %s is error!It\'s done.Hurry up to restart,Jiecao Wu' %error_ip
    msg = MIMEText(content)
    msg['From'] = mail_address.mail_user
    msg['Subject'] = 'warnning %s'%error_ip
    msg['To'] = mail_address.mail_to

    if error_ip == '100.0.0.86':
        try:
            s = smtplib.SMTP()
            s.connect(mail_address.mail_host)
            s.login(mail_address.mail_user,mail_address.mail_pwd)
            s.sendmail(mail_address.mail_user,[mail_address.mail_to,mail_address.mail_cc],msg.as_string())
            s.close()
        except Exception ,e:
            print e

    if error_ip != '100.0.0.86':
        try:
            s = smtplib.SMTP()
            s.connect(mail_address.mail_host)
            s.login(mail_address.mail_user,mail_address.mail_pwd)
            s.sendmail(mail_address.mail_user,[mail_address.mail_cc,mail_address.mail_cc],msg.as_string())
            s.close()
        except Exception ,e:
            print e

 

def check(get_ip):
    '''
    检测模块
    '''
    try :
        ping=pexpect.spawn("ping -c1 %s" % (get_ip))
        check_result =ping.expect(["Request","(?i)time=",pexpect.EOF, pexpect.TIMEOUT],)
    except :
        check_result = 0
    return check_result
 

def main():
    mail_address = InitSetting("setting.ini")
    mail_address.loading_ini
    while True :
        for i in check_ip:
            check_status = check("%s"%i)
            if check_status == 1:
                check_ip["%s"%i] = 0
            else :
                check_ip["%s"%i] +=1

            if check_ip["%s"%i] in send_mail_limit :
                mail_warn(i,mail_address)
        time.sleep(60)


 
if __name__ == "__main__":
    main()