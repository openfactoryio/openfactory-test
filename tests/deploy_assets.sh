#!/usr/bin/env bash

# Deploy Assets for tests
ofa apps up /workspaces/openfactory-test/ressources/apps/demo
ofa apps up /workspaces/openfactory-test/ressources/apps/fastapiDemo
ofa device up /workspaces/openfactory-test/ressources/devices

sleep 2
ofa asset ls
