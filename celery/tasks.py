import os
import time
from celery import Celery
from flask_socketio import SocketIO

env = os.environ
CELERY_BROKER_URL = env.get('CELERY_BROKER_URL', 'amqp://guest:guest@rabbitmq:5672/'),
CELERY_RESULT_BACKEND = env.get('CELERY_RESULT_BACKEND', 'rpc://')


celery = Celery('tasks',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)

socketio = SocketIO(message_queue='amqp://admin:admin123@rabbitmq:5672/socketio')


def send_message(event: str, message: dict, room: str):
    socketio.emit(event, message, room=room)


@celery.task(name="tasks.external_api_call")
def external_api_call(data, room):
    time.sleep(2)
    send_message("API_RESULT_AVAILABLE", {"data": data}, room)
