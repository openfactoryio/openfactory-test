#!/bin/bash

# Remove assets
./tests/teardown_assets.sh

# Remove virtual NFS server
echo "🛑 Removing virtual NFS server"
openfactory-stop-nfs

# Remove connectors
echo "🛑 Removing OPC UA connector"
ofa apps down /usr/local/share/openfactory-connectors/app_opcua_connector.yml
echo "🛑 Removing SHDR connector"
ofa apps down /usr/local/share/openfactory-connectors/app_shdr_connector.yml

# Teardown infrastructure
/usr/local/bin/teardown.sh

# Remove virtual devices
echo "🛑 Removing virtual sensors"
docker rm -f virtual-opcua-sensor virtual-opcua-barcode-reader
