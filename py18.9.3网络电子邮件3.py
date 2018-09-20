#  py18.9.1网络电子邮件3
#  发送附件,会这个就可以批量发邮件了

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr

import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


#  邮件对象：
from_addr = input('From:')
password = input('Password:')
to_addr = input('To:')
smtp_server = input('SMTP server:')


msg = MIMEMultipart()
msg['From'] = _format_addr('Python爱好者<%s>' % from_addr)
msg['To'] = _format_addr('管理员<%s>' % to_addr)
msg['Subject'] = Header('来自SMTP的问候...', 'utf-8').encode()

# 邮件正文是MIMEText:
msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))

# 添加附件就是加上一个MIMEBase，从本地读取一个照片
with open('D:/life/wallpaper/女隐.jpg', 'rb') as f:
    # 设置邮件的MIME和文件名，这里是JPG类型
    mime = MIMEBase('image', 'jpg', filename='女隐.jpg')
    # 加上必要的头信息：
    mime.add_header('Content-Disposition', 'attachment', filename='女隐.jpg')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来
    mime.set_payload(f.read())
    # 用Base64编码：
    encoders.encode_base64(mime)
    # 添加到MIME Multi part：
    msg.attach(mime)

server = smtplib.SMTP_SSL(smtp_server, 587)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
