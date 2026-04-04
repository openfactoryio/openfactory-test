#!/bin/bash

# Build demo-app
cd ressources/apps/demo
docker build --build-arg OFA_VERSION="v$OPENFACTORY_VERSION" -t demo-app -f Dockerfile .
cd /workspaces/openfactory-test
