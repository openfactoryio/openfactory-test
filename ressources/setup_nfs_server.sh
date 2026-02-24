#!/usr/bin/env bash
: '
Script to set up an NFS server container in Docker.

This script performs the following tasks:

1. Ensures a Docker network named "factory-net" exists; creates it if missing.
2. Checks for the presence of an NFS server container (`devcontainer-nfs`):
   - If the container does not exist:
     - Creates a Docker volume (`devcontainer-nfsdata`) for NFS storage.
     - Starts a new NFS server container using `itsthenetwork/nfs-server-alpine`.
     - Configures the container to be privileged, expose NFS ports, and restart unless stopped.
   - If the container exists:
     - Starts it if it is not already running.
3. Creates a mount point `/exports/home/ofa/nfsvolume` inside the NFS container.

Variables:

- NFS_CONTAINER_NAME: Name of the NFS server container (`devcontainer-nfs`).
- NFS_VOLUME_NAME: Name of the Docker volume used for NFS data (`devcontainer-nfsdata`).

Usage:

    ./setup-nfs.sh

Requirements:

- Docker must be installed and running.
- The user must have permissions to manage Docker containers and networks.
- The NFS server image `itsthenetwork/nfs-server-alpine` must be available (pulled automatically if missing).

Mount NFS volume:

To mount into the devcontainer the NFS volume (adjust mount point as desired):

     sudo mount -t nfs ${CONTAINER_IP}:/home/ofa/nfsvolume /workspaces/openfactory-test/nfs/
'
set -e

NFS_CONTAINER_NAME=devcontainer-nfs
NFS_VOLUME_NAME=devcontainer-nfsdata

echo "⚙️ Creating virtual NFS server..."

# Create factory-net network if it doesn't exist
if ! docker network inspect factory-net >/dev/null 2>&1; then
    echo "🔗 Creating factory-net network..."
    docker network create \
      --driver bridge \
      --label com.docker.compose.network="factory-net" \
      factory-net
else
    echo "✅ factory-net network already exists, skipping creation."
fi

echo "🔍 Checking for NFS server container..."

if ! docker ps -a --format '{{.Names}}' | grep -q "^${NFS_CONTAINER_NAME}$"; then
  echo "📦 Creating NFS Docker volume..."
  docker volume create ${NFS_VOLUME_NAME}

  echo "🚀 Starting NFS server container..."
  docker run -d \
    --name ${NFS_CONTAINER_NAME} \
    --privileged \
    -e SHARED_DIRECTORY=/exports \
    -v ${NFS_VOLUME_NAME}:/exports \
    -p 111:111/tcp \
    -p 111:111/udp \
    -p 2049:2049/tcp \
    -p 2049:2049/udp \
    --network factory-net \
    --restart unless-stopped \
    itsthenetwork/nfs-server-alpine
else
  echo "▶ NFS container already exists, starting if needed..."
  docker start ${NFS_CONTAINER_NAME} >/dev/null 2>&1 || true
fi

# create mount point in server
echo "📁 Creating NFS mountpoint in NFS server..."
docker exec ${NFS_CONTAINER_NAME} mkdir -p /exports/home/ofa/nfsvolume

# mount it like so
# sudo mount -t nfs ${CONTAINER_IP}:/home/ofa/nfsvolume /workspaces/openfactory-test/nfs/
# adjust mount point as needed