FROM python:3.7-slim
USER root

ENV APP /app

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    locales \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    python3-pyqt5 \
    vim less \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm
ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal
ENV SHAPE_ENCODING shift-jis

WORKDIR $APP

RUN pip3 install --upgrade pip setuptools

COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
