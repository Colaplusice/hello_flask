from datetime import timedelta

BROKER_URL = "redis://localhost:6379/0"

CELERY_RESULT_BACKEND = "redis://localhost:6379/1"

CELERY_ACCEPT_CONTENT = ["json"]

# debug
CELERY_TASK_ALWAYS_EAGER = True
# 任务调度 没十分钟跑次
CELERYBEAT_SCHEDULE = {
}
