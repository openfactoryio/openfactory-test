#!/bin/bash

# deploy assets
./tests/deploy_assets.sh

# run tests
pytest tests
