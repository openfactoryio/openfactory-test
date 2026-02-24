# openfactory-test
Minimal repo to verify if a release was succesfull

## Deploy OpenFactory
```bash
./start_test_env.sh
```

## Deploy some assets
```bash
./tests/deploy_assets.sh
```

## Subscribe to a deployed asset
```bash
python ./tests/subscribe_to_assets.py
```
