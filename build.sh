#!/bin/bash

cd /root/Routines/Milhos/PostgresqlSnapshotManager
git pull origin main
. ./set_env_variables.sh
python3 main.py
