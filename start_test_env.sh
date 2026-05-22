#!/bin/bash

# Add some virtual sensors
echo "🚀 Deploying virtual sensors"
docker run -d --name virtual-opcua-sensor -p 4840:4840 -e NUM_SENSORS=2 ghcr.io/openfactoryio/virtual-opcua-sensor:$OPENFACTORY_VERSION
docker run -d -p 4841:4840 --name virtual-opcua-barcode-reader ghcr.io/openfactoryio/virtual-opcua-barcode-reader:$OPENFACTORY_VERSION

# Setup infrastructure
/usr/local/bin/spinup.sh

# Setup OPC UA connectors
docker compose -f /usr/local/share/openfactory-opcua/docker-compose.yml up -d

# Build apps
./build_apps.sh

# Setup virtual NFS server
openfactory-start-nfs
