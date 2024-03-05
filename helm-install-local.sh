#!/bin/bash

## Ensure helm is installed and available via PATH
if ! command -v helm &> /dev/null; then
  echo "Helm not found in PATH. Please install helm (brew install helm) or add it to PATH."
  exit 1
fi

## Ensure that the user is in their local cluster. If not, exit
CLUSTER=$(kubectl config current-context)

if [[ "$CLUSTER" != "docker-desktop" ]]; then

  echo "This script should only be used for your local environment, a.k.a. docker-desktop."
  echo "Your current context: ${CLUSTER}."
  echo ""
  echo "To set your context to local, use the following command: kubectl config use-context docker-desktop"
  exit 1

fi

HELM_DIR="./helm/metro2"

RELEASE=${RELEASE:-metro2}

# Build Dependency Charts
if [ ! -d .helm/metro2/charts ]; then
  echo "Building dependency charts..."
  helm repo update
  helm dependency build ./helm/metro2
else
  if [ -z $SKIP_DEP_UPDATE ]; then
    helm dependency update ./helm/metro2
  fi
fi


helm install metro2-db \
bitnami/postgresql --set persistence.enabled=false \
--set auth.postgresPassword='cfpb' \
--set auth.database='metro2-data' \
--set auth.host='metro2-db-postgresql' \
--set auth.user='postgres'


# wait for postgres to be in ready state
kubectl wait --for=condition=ready \
--all pods

VALUES="values-local.yaml"

helm upgrade --install $RELEASE $HELM_DIR -f $HELM_DIR/$VALUES

