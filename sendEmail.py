#!/usr/bin/env python3
# -*- coding:utf-8 -*-

################################################################################################
# method1
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def sendEmail():
    '''send email.'''
    mail_host = "smtp.163.com"   # 邮箱服务器，qq邮箱为 'smtp.qq.com',若出现域名无法解析，可直接用ip地址
    mail_user = "发件人邮箱"
    mail_pass = "***"  # 开通SMTP服务时的授权码
    sender = "发件人邮箱"
    receivers = ['***@**.com'] # 收件人邮箱，可有多个
    ###添加邮件文本内容
    msg_txt = ''' mail contents''' # 邮件内容
    main_text = MIMEText(msg_txt, 'plain', 'utf-8')   # 邮件中的文本内容
    message = MIMEMultipart()
    message.attach(main_text)
    ###添加邮件附件,各种格式的文件以及照片都可以以这种形式添加
    file=MIMEApplication(open(file,"rb").read())
    file.add_header('Content-Disposition', 'attachment', filename='filename')
    message.attach(file)
    ###发送邮件
    title = "邮件主题"
    message['Subject'] = Header(title, 'utf-8') # 邮件主题
    message['From'] = Header("发件人名称", 'utf-8') # 显示发送人
    message['To'] = Header("***", 'utf-8')  # 显示收件人
    # 连接登录服务器并发送邮件    
    smtpObj = smtplib.SMTP(mail_host)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())

    print('Email has been sent successfully!')

if __name__=='__main__':
    sendEmail()



##################################################################################
# method2 
import yagmail

def sendEmail(contents, receivers, user='humaninfo@novogene.com', password='***', host='smtp.qq.com', port=465, subject='reminder'):
    '''send email.'''
    yag = yagmail.SMTP(user=user, password=password, host=host, port=port)
    yag.send(to=receivers, subject=subject, contents=contents)
    print('Email has been sent!')

if __name__=='__mail__':
    contents = ["hello", picture, pdf_file] # 邮件内容及附件，可自动识别
    receivers = ['a@qq.com','b@qq.com'] #收件人
    sendEmail(contents,receivers)