import json
from flask import Flask, request, make_response
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
from celery_worker import celery

# the app is an instance of the Flask class
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'there is no secret'
socketio = SocketIO()

# integrates Flask-SocketIO with the Flask application
socketio.init_app(app, message_queue='amqp://admin:admin123@rabbitmq:5672/socketio', cors_allowed_origins='http://localhost:3000')

# POST data using /external endpoint, need room as url param to uniquely identify the user
@app.route('/external', methods=["POST"])
def call_external_api():
    data = request.get_json()
    room = request.args.get("room")
    celery.send_task('tasks.external_api_call', args=[data, room], kwargs={})
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@socketio.on('connect')
def socket_connect():
    emit('connected', {'data': 'Connected'})


@socketio.on('join_room')
def on_join(room):
    join_room(room)
    emit('joined_room', {'data': 'Joined Room %s' % room})
