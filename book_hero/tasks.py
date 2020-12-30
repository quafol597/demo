from datetime import datetime
from demo.celery import app as celery_app


@celery_app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@celery_app.task(name='print_strftime')
def print_strftime():

    strftime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    a = "这里是BookModelViewSet_list视图, 我在发布'print_strftime'异步任务."
    print(a)

    return f"haha{strftime}"
