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
 

#### 配置服务器IP地址
check_ip ={"192.168.1.200":0,}
#### 定义几次ping不通发邮件
send_mail_limit = [3，10]
#### 发邮件的邮件服务器配置
mail_host = 'smtp.163.com'
mail_user = 'testing_007@163.com'
mail_pwd = 'testing'
mail_to = "wuxiaoning@dayang.com.cn"
mail_cc = "testing_007@163.com"


#####
##发送模块
#####
 
def mail_warn(error_ip):
    content = 'Ping IP %s is error!It\'s done.Hurry up to restart,Jiecao Wu' %error_ip
    msg = MIMEText(content)
    msg['From'] = mail_user
    msg['Subject'] = 'warnning %s'%error_ip
    msg['To'] = mail_to
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pwd)
        s.sendmail(mail_user,[mail_to,mail_cc],msg.as_string())
        s.close()
    except Exception ,e:
        print e
 
 #####
 ##检测模块
 #####
def check(get_ip):
    try :
        ping=pexpect.spawn("ping -c1 %s" % (get_ip))
        check_result =ping.expect(["Request","(?i)time=",pexpect.EOF, pexpect.TIMEOUT],)
    except :
        check_result = 0
    return check_result
 

#####
##主程序
#####
def main():
##  try_num=1
    while True :
        for i in check_ip:
##          print try_num
            check_status = check("%s"%i)
##          print check_status
##          try_num+=1
            if check_status == 1:
                check_ip["%s"%i] = 0
            else :
                check_ip["%s"%i] +=1
            if check_ip["%s"%i] in send_mail_limit :
                mail_warn("%s"%i)

##              print "once over"
        time.sleep(10)
 
if __name__ == "__main__":
    main()