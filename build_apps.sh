#!/bin/bash

# Build demo-app
cd ressources/apps/demo
docker build --build-arg OFA_VERSION="$OPENFACTORY_VERSION" -t demo-app -f Dockerfile .
cd /workspaces/openfactory-test

# Build demo-fastapi-app
cd ressources/apps/fastapiDemo
docker build --build-arg OFA_VERSION="$OPENFACTORY_VERSION" -t demo-fastapi-app -f Dockerfile .
cd /workspaces/openfactory-test

# Build demo-flask-app
cd ressources/apps/flaskDemo
docker build --build-arg OFA_VERSION="$OPENFACTORY_VERSION" -t demo-flask-app -f Dockerfile .
cd /workspaces/openfactory-test
