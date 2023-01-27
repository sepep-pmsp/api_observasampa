#! /bin/bash

git pull

python startup.py

#tenta criar o ambiente. vai falhar se ja existir
set +e
python -m venv venv
set -e

source venv/bin/activate

pip install -r requirements.txt

touch -a api_log.txt

uvicorn api:app --host 0.0.0.0 --port 80 --log-config api_log.txt