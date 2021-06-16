#!/bin/bash
set -e
psql -U postgres <<EOSQL
  CREATE DATABASE autopolygon_api WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'ja_JP.UTF-8' LC_CTYPE = 'ja_JP.UTF-8';
EOSQL
