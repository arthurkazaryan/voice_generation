from api.worker import app
from celery.utils.log import get_task_logger
import sys
import os

celery_log = get_task_logger(__name__)
sys.path.append(os.getcwd())


@app.task(name='generation')
def run_generation(voice: str, text: str):
    from generation_predict import predict

    celery_log.info(f'Task received.\nVoice: {voice}\nText: {text}')

    file_path = predict(
        voice=voice,
        text=text,
    )

    return file_path
