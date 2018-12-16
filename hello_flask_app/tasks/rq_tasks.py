# encoding=utf-8
from hello_flask_app import create_app
from rq import get_current_job
import sys
from hello_flask_app.models import Task, Post
from hello_flask_app.models import User
from hello_flask_app import db

import time

app = create_app("default")
# 推送上下文，让这个app成为current_app
# 这样sqlalchemy才会获得到配置
app.app_context().push()


def _set_task_progress(progress):
    # 通过当前上下文来得到 当前的job_id

    job = get_current_job()
    if job:
        job.meta["progress"] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        # 调用user对象的这个方法
        if task:
            task.user.add_notification("task_process", {"task.id": task.user_id})
            if progress >= 100:
                task.complete = True
            db.session.commit()
        else:
            print("task is None")


def export_posts(user_id):
    try:
        user = User.query.get(user_id)
        print(user)
        _set_task_progress(0)
        data = []
        i = 0
        total_post = user.posts.count()
        print("totoal count:{}".format(total_post))
        for post in user.posts.order_by(Post.timestamp.asc()):
            data.append(
                {
                    "title": post.title,
                    "body": post.body,
                    "timestamp": post.timestamp.isoformat() + "Z",
                }
            )
            i += 1
            print(i)
            time.sleep(5)
        _set_task_progress(i * 100 // total_post)

    except Exception as e:
        # 从数据库中删除任务
        # print('出错啦'*20)
        print(e.args)
        tasks = Task.query.filter_by(user=user).first()
        db.session.delete(tasks)
        db.session.commit()
        _set_task_progress(100)
        app.logger.error("unhandled exception", exc_info=sys.exc_info())


def example(seconds):
    job = get_current_job()
    print("Starting task")
    for i in range(seconds):
        job.meta["progress"] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta["progress"] = 100
    job.save_meta()
    print("Task completed")
