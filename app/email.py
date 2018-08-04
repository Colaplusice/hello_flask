# encoding=utf-8
from flask_mail import Mail, Message
from flask import current_app, render_template
from threading import Thread
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# 创建线程，异步发送邮件
def send_email(to, subject, template, sync=False, attachments=None, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' '
                  + subject, sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    # 添加附件
    if attachments:
        msg.attach(*attachments)
    if sync:
        mail.send(msg)

        # 异步发送
    else:
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return thr
