#!/bin/bash
while ! nc -z tcph-db 5432; do sleep 3; done
python client.py --host=0.0.0.0