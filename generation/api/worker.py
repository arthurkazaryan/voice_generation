from celery import Celery


app = Celery(
    'generation',
    broker='redis://redis:6379/',
    backend='redis://redis:6379/',
    include=['generation.api.tasks']
)

app.conf.task_track_started = True
