#!/bin/bash

# Remove OPC UA connectors
docker compose -f /usr/local/share/openfactory-opcua/docker-compose.yml down

# Teardown infrastructure
/usr/local/bin/teardown.sh

# Remove virtual devices
echo "🛑 Removing virtual sensors"
docker stop virtual-opcua-sensor
docker stop virtual-opcua-barcode-reader
docker rm virtual-opcua-sensor virtual-opcua-barcode-reader
