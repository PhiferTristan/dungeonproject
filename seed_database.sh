#!/bin/bash

rm db.sqlite3
rm -rf ./dungeonapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations dungeonapi
python3 manage.py migrate dungeonapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata dungeonmasterusers
python3 manage.py loaddata playerusers
python3 manage.py loaddata races
python3 manage.py loaddata alignments