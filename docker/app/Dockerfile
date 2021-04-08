FROM python:3.7-alpine
USER root

ENV APP /app

RUN apt-get update \
    && apt-get -y --no-install-recommends apt-utils \
    locales \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm
ENV SHAPE_ENCODING shift-jis

WORKDIR $APP

RUN pip install --upgrade pip

COPY requirements.txt $APP
RUN pip3 install -r $APP/requirements.txt
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
