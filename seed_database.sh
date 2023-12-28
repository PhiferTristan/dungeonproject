#!/bin/bash

rm db.sqlite3
rm -rf ./dungeonapi/migrations
python3 manage.py makemigrations admin
python3 manage.py makemigrations dungeonapi
python3 manage.py migrate
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata dungeon_master_users
python3 manage.py loaddata player_users
python3 manage.py loaddata races
python3 manage.py loaddata alignments
python3 manage.py loaddata backgrounds
python3 manage.py loaddata languages
python3 manage.py loaddata skills
python3 manage.py loaddata abilities
python3 manage.py loaddata saving_throws
python3 manage.py loaddata flaws
python3 manage.py loaddata ideals
python3 manage.py loaddata bonds
python3 manage.py loaddata personality_traits
python3 manage.py loaddata dndclasses
python3 manage.py loaddata subclasses
python3 manage.py loaddata characters
python3 manage.py loaddata character_ability_scores
python3 manage.py loaddata character_saving_throws
python3 manage.py loaddata character_skills
python3 manage.py loaddata character_backgrounds
python3 manage.py loaddata character_flaws
python3 manage.py loaddata character_ideals
python3 manage.py loaddata character_bonds
python3 manage.py loaddata character_personality_traits