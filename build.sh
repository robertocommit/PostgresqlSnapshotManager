#!/bin/bash

cd /root/valpiccola/PostgresqlSnapshotManager
git pull origin main
. ./set_env_variables.sh
python3 main.py
