FROM python:3-alpine3.10

WORKDIR app/

COPY . .


RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    && pip install -r requirements.txt
#RUN pip install --upgrade pip --no-cache-dir
#RUN pip install -r requirements.txt

ENTRYPOINT python

CMD ['manage.py', 'runserver']
