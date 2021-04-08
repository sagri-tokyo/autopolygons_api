FROM python:3.7
USER root

RUN python3 --version

ENV APP /app

RUN apt-get update
RUN apt-get -y install locales && \
  localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get install -y binutils libproj-dev gdal-bin libgdal-dev python3-pyqt5

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm
ENV SHAPE_ENCODING shift-jis
ENV DJANGO_READ_ENV_FILE True

WORKDIR $APP
RUN apt-get install -y vim less

RUN pip install --upgrade pip
RUN pip3 install --upgrade setuptools

COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
