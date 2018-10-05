# encoding=utf-8
from flask import jsonify
from app.extensions import celery
from .models import *
import time
from . import mail
from app.main import main
from flask_mail import Message
from flask import current_app, render_template


# 创建线程，异步发送邮件
@celery.task
def send_email(to, subject, template, attachments=None, **kwargs):
    app = current_app._get_current_object()

    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' '
                  + subject, sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    with app.app_context():
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
    time.sleep(2)
    # 添加附件
    if attachments:
        msg.attach(*attachments)
    mail.send(msg)


@celery.task(bind=True)
def export_async_posts(self, *args):
    user_id = args[0]
    user = User.query.get(user_id)
    data = []
    i = 0
    total_post = user.posts.count()
    for post in user.posts.order_by(Post.timestamp.asc()):
        data.append({
            'title': post.title,
            'body': post.body,
            'timestamp': post.timestamp.isoformat() + 'Z'
        })
        self.update_state(
            state='PROGRESS',
            meta={
                'current': i, 'total': total_post,
                'status': 'post'
            }
        )
        i += 1
        time.sleep(5)
    return {'current': total_post, 'total': total_post, 'status': 'Task completed!'}


@celery.task
def change_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    task.complete = True
    db.session.add(task)


@celery.task
def example(seconds):
    print('Starting task')
    for i in range(seconds):
        time.sleep(1)
    print('task finished')
