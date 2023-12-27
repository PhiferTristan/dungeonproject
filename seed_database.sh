#!/bin/bash

rm db.sqlite3
rm -rf ./dungeonapi/migrations
python3 manage.py makemigrations admin
python3 manage.py makemigrations dungeonapi
python3 manage.py migrate
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata dungeonmasterusers
python3 manage.py loaddata playerusers
python3 manage.py loaddata races
python3 manage.py loaddata alignments
python3 manage.py loaddata backgrounds
python3 manage.py loaddata languages
python3 manage.py loaddata skills
python3 manage.py loaddata abilities
python3 manage.py loaddata savingthrows
python3 manage.py loaddata flaws
python3 manage.py loaddata ideals
python3 manage.py loaddata bonds
python3 manage.py loaddata personalitytraits
python3 manage.py loaddata dndclasses
python3 manage.py loaddata subclasses
python3 manage.py loaddata characters
python3 manage.py loaddata characterabilityscores