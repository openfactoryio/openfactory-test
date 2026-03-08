#!/bin/bash

# Add some virtual sensors
echo "🚀 Deploying virtual sensors"
docker run -d --name virtual-opcua-sensor -p 4840:4840 -e NUM_SENSORS=2 ghcr.io/openfactoryio/virtual-opcua-sensor
docker run -d -p 4841:4840 --name virtual-opcua-barcode-reader ghcr.io/openfactoryio/virtual-opcua-barcode-reader

# Setup infrastructure
/usr/local/bin/spinup.sh

# Setup OPC UA connectors
docker compose -f /usr/local/share/openfactory-opcua/docker-compose.yml up -d

# Build demo-app
cd ressources/apps/demo
docker build --build-arg OFA_VERSION="v$OPENFACTORY_VERSION" -t demo-app -f Dockerfile .
cd /workspaces/openfactory-test

# Setup virtual NFS server
./ressources/setup_nfs_server.sh
