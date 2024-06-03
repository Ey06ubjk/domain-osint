#!/bin/sh
# Generate a random secret key
export FLASK_SECRET_KEY=$(python -c 'import os; print(os.urandom(24).hex())')

# Execute the CMD from the Dockerfile
exec "$@"
