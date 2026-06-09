#!/bin/bash

echo "🏭 Building OpenFactory Applications for tests..."

# Build demo-app
echo "🏭 Building DEMO-APPs..."
cd ressources/apps/demo
docker build --build-arg OFA_VERSION="$OPENFACTORY_VERSION" -t demo-app -f Dockerfile .
cd /workspaces/openfactory-test

# Build demo-fastapi-app
echo "🏭 Building DEMO-FASTAPI-APP..."
cd ressources/apps/fastapiDemo
docker build --build-arg OFA_VERSION="$OPENFACTORY_VERSION" -t demo-fastapi-app -f Dockerfile .
cd /workspaces/openfactory-test

# Build demo-flask-app
echo "🏭 Building DEMO-FLASK-APP..."
cd ressources/apps/flaskDemo
docker build --build-arg OFA_VERSION="$OPENFACTORY_VERSION" -t demo-flask-app -f Dockerfile .
cd /workspaces/openfactory-test
