FROM postgres:12

LABEL maintainer="PostGIS Project - https://postgis.net"

RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG="ja_JP.UTF-8" \
	LANGUAGE="ja_JP:ja" \
	LC_ALL="ja_JP.UTF-8"
ENV POSTGIS_MAJOR 3
ENV POSTGIS_VERSION 3.1.2+dfsg-1~exp2.pgdg100+1

RUN apt-get update \
	&& apt-cache showpkg postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR \
	&& apt-get install -y --no-install-recommends \
	postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR=$POSTGIS_VERSION \
	postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts=$POSTGIS_VERSION \
	&& rm -rf /var/lib/apt/lists/*

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./initdb-postgis.sh /docker-entrypoint-initdb.d/10_postgis.sh
COPY ./update-postgis.sh /usr/local/bin
COPY ./postgres/docker-entrypoint-initdb.d/init.sh .
