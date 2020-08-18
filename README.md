To run:
```bash
docker-compose build
docker-compose up -d # run in detached mode
```

React front-end serves a single page which has an option to send a POST request to backend running on Flask. This POST request always returns a success status and the task is submitted to Celery via RabbitMQ. Celery executes the task and send the data to events managed by SocketIO. React picks up the event and shows the results in frontend.

Alpine versions of Linux is used to keep the image size small.


- `http://localhost:3000` for the front end in React which only has one text box to give input to POST request and returns whatever data you send

- `http://localhost:5000` for the back end (Flask - CORS, socketio / celery / rabbitmq / worker tasks)
- `http://localhost:15672` for rabbitmq-management
