import smtplib
from email.mime.text import MIMEText
from email.header import Header

import logging
logger = logging.getLogger("re")

SENDER = 'computation_report@raganetwork.com'
PASSWORD = 'wh5mGCjikxxycJWU'

SMTP_SERVER = 'smtp.exmail.qq.com'
SMTP_PORT = 465

class EmailReporter:
    def __init__(self, 
        receiver: str,
    ) -> None:
        self.receiver = receiver

    def fill_message(self, 
        subject,
        message_content
    ):
        message = MIMEText(message_content, 'plain', 'utf-8')
        message['From'] = SENDER
        message['To'] = self.receiver
        message['Subject'] = subject if subject is not None else "服务器资源用量警告"
        self.message = message

    def send(self):
        try:
            smtpObj = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
            smtpObj.login(SENDER, PASSWORD)
            smtpObj.sendmail(SENDER, self.receiver, self.message.as_string())
            logger.info("邮件发送成功, 收件人: %s" % self.receiver)
        except Exception as e:
            logger.error("邮件发送失败, 收件人: %s" % self.receiver)
            logger.error(e)
        finally:
            smtpObj.quit()