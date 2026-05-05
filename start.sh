#!/bin/sh

flask db upgrade
python -m app.seed
gunicorn run:app --bind 0.0.0.0:5000