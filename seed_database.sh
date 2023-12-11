#!/bin/bash

rm db.sqlite3
rm -rf ./dungeonapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations dungeonapi
python3 manage.py migrate dungeonapi