from datetime import timedelta

# redi 作为消息队列
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['pickle']

# 任务调度 没十分钟跑次
CELERYBEAT_SCHEDULE = {

    'add': {

        'task': 'celery_beat.tasks.add',

        'schedule': timedelta(seconds=10),

        'args': (14, 14)

    },
    'send_email': {
        'task': 'app.play.views.send_async_email',
    }

}
