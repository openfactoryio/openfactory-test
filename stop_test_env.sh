#!/bin/bash

# Remove assets
./tests/teardown_assets.sh

# Remove virtual NFS server
echo "🛑 Removing virtual NFS server"
openfactory-stop-nfs

# Remove OPC UA connector
echo "🛑 Removing OPC UA connector"
docker compose -f /usr/local/share/openfactory-opcua/docker-compose.yml down

# Teardown infrastructure
/usr/local/bin/teardown.sh

# Remove virtual devices
echo "🛑 Removing virtual sensors"
docker rm -f virtual-opcua-sensor virtual-opcua-barcode-reader
