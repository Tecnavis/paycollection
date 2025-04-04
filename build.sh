#!/bin/bash

# Exit immediately if a command fails
set -e 

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Making migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

echo "Creating roles and permissions..."
python manage.py create_roles_and_permissions
