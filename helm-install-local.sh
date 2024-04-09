#!/bin/bash

BLUE='\033[0;34m'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'
LOCAL_CLUSTER=docker-desktop

## Ensure helm is installed and available via PATH
if ! command -v helm &> /dev/null; then
  echo "Helm not found in PATH. Please install helm (brew install helm) or add it to PATH."
  exit 1
fi

## Ensure that the user is in their local cluster. If not, exit
CLUSTER=$(kubectl config current-context)

if [[ "$CLUSTER" != "docker-desktop" ]]; then
  echo ""
  echo -e "This script should only be used for your local environment: the ${BLUE}$LOCAL_CLUSTER${NC} cluster."
  echo -e "Your current context: ${RED}${CLUSTER}${NC}."
  echo ""
  echo ""
  echo -e "Switching to ${BLUE}$LOCAL_CLUSTER${NC}"
  KUBECTL_OUTPUT=$(kubectl config use-context $LOCAL_CLUSTER 2>&1)
  KUBECTL_EXIT_CODE=$?

  # Check exit code
  if [[ "$KUBECTL_EXIT_CODE" -ne 0 ]]; then
    echo -e "${RED}Error:${NC} kubectl command failed with exit code $KUBECTL_EXIT_CODE"
    echo -e "${RED}Output:${NC} $KUBECTL_OUTPUT"
    echo "Exiting helm-install-local"
    exit 1
  else
   echo -e "${GREEN}Success:${NC} Switched to ${BLUE}$LOCAL_CLUSTER${NC} cluster"
   echo ""
  fi 

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

