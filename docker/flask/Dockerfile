FROM python:stretch

RUN pip install uwsgi
RUN mkdir /app
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
COPY docker/flask/uwsgi.ini .
RUN apt-get install -yq gdal-bin python-gdal
CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]
