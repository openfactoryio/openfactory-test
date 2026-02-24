#!/usr/bin/env bash

# Deploy Assets for tests
ofa apps up /workspaces/openfactory-test/ressources/apps/demo
ofa device up /workspaces/openfactory-test/ressources/devices

sleep 2
ofa asset ls
