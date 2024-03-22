import os
import time
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
# app.conf.update({
#     'broker_url': 'amqp://guest:guest@broker:5672//',
#     'result_backend': 'db+postgresql://postgres:supersecreatpassword@db:5432/app',
#     'database_table_schemas' : {
#         'task': 'celery',
#         'group': 'celery',
#     },
#     'database_table_names' : {
#         'task': 'myapp_taskmeta',
#         'group': 'myapp_groupmeta',
#     }
# })

# app.conf.timezone = 'Asia/Dhaka'
# app.result_backend = 'postgresql://postgres:supersecreatpassword@db:5432/app'

# app.database_table_schemas = {
#     'task': 'celery',
#     'group': 'celery',
# }

# app.database_table_names = {
#     'task': 'myapp_taskmeta',
#     'group': 'myapp_groupmeta',
# }

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.loader.override_backends['django-db'] = 'django_celery_results.backends.database:DatabaseBackend'

# Load task modules from all registered Django apps.
app.autodiscover_tasks()



# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

@app.task
def add(x,y):
    time.sleep(20)
    return x+y