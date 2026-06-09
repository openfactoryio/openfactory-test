#!/bin/bash

# Add some virtual sensors
echo "🚀 Deploying virtual sensors"
docker run -d -p 4840:4840 --name virtual-opcua-sensor -e NUM_SENSORS=2 ghcr.io/openfactoryio/virtual-opcua-sensor:$OPENFACTORY_VERSION
docker run -d -p 4841:4840 --name virtual-opcua-barcode-reader ghcr.io/openfactoryio/virtual-opcua-barcode-reader:$OPENFACTORY_VERSION
docker run -d -p 7878:7878 --name virtual-shdr-sensor ghcr.io/openfactoryio/virtual-temp-sensor:$OPENFACTORY_VERSION

# Setup infrastructure
/usr/local/bin/spinup.sh

# Setup connectors
ofa apps up /usr/local/share/openfactory-connectors/app_opcua_connector.yml
ofa apps up /usr/local/share/openfactory-connectors/app_shdr_connector.yml

# Build apps
./build_apps.sh

# Setup virtual NFS server
openfactory-start-nfs
