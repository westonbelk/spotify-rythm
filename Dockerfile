FROM python:alpine

RUN apk add gcc musl-dev libffi-dev make

RUN mkdir /app
RUN adduser -h /app -s /bin/false -D -u 1001 app
RUN chown -R app:app /app
WORKDIR /app
USER app

ADD --chown=app:app src/requirements.txt /app/
RUN pip install -r requirements.txt

ADD --chown=app:app src/*.py /app/

ENTRYPOINT ["python", "main.py"]