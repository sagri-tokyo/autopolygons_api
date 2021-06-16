#! /bin/bash

set -e
psql -U postgres -d $1 <<EOSQL
  DELETE FROM farmlands;
  SELECT setval(pg_get_serial_sequence('"farmlands"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "farmlands";
EOSQL
