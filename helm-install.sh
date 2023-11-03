#!/bin/bash

#!/bin/bash

## Ensure helm is installed and available via PATH
if ! command -v helm &> /dev/null; then
  echo "Helm not found in PATH. Please install helm (brew install helm) or add it to PATH."
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


## Get Cluster
CLUSTER=$(kubectl config current-context)

if [[ "$CLUSTER" == "docker-desktop" ]]; then 

  helm install metro2-db \
  --set auth.postgresPassword='cfpb' \
  --set auth.database='metro2-data' \
  bitnami/postgresql --set persistence.enabled=false

  # wait for postgres to be in ready state
  kubectl wait --for=condition=ready \
  --all pods

  VALUES="values.yaml"

else 

  VALUES="eks-values.yaml"

fi

helm upgrade --install $RELEASE $HELM_DIR -f $HELM_DIR/$VALUES

