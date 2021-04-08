set -e
psql postgres << EOSQL
  CREATE DATABASE autopolygon_api WITH OWNER = admin TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'ja_JP.UTF-8' LC_CTYPE = 'ja_JP.UTF-8';
EOSQL
