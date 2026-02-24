#!/bin/bash

# Remove assets
./tests/teardown_assets.sh

# Remove virtual NFS server
echo "🛑 Removing virtual NFS server"
docker rm -f devcontainer-nfs
docker volume rm devcontainer-nfsdata

# Remove OPC UA connectors
docker compose -f /usr/local/share/openfactory-opcua/docker-compose.yml down

# Teardown infrastructure
/usr/local/bin/teardown.sh

# Remove virtual devices
echo "🛑 Removing virtual sensors"
docker rm -f virtual-opcua-sensor virtual-opcua-barcode-reader
