#!/bin/bash

echo "Generating sql..."
row_count=$1
python3 ./generate_data.py ${row_count:=1000} > ./sql/populate.sql
echo "SQL generated"

docker-compose up
