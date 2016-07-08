FROM python:3.5
ENV PYTHONUNBUFFERED 1

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD . /app
WORKDIR /app

EXPOSE 8000
CMD ["/app/compose/start.sh"]
