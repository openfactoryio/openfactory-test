# openfactory-test
Minimal repo to verify if a release was succesfull

## Deploy OpenFactory
```bash
spinup
opcua-connector-up
```

## Deploy some assets
```bash
# Deploy virtual OPC UA devices
docker run -d --name virtual-opcua-sensor -p 4840:4840 -e NUM_SENSORS=2 ghcr.io/openfactoryio/virtual-opcua-sensor
# Deploy them in OpenFactory
ofa device up ressources/devices.yml
```

## Subscribe to a deployed asset
```bash
python subscribe_to_assets.py
```
