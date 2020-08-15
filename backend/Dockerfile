FROM python:3.7-alpine

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
     && pip install eventlet==0.26.1 \
     && apk del .build-deps gcc musl-dev

CMD ["gunicorn", "-c", "config.py", "main:app"]