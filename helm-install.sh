#!/bin/bash

# Flags

## Option to skip --wait and set timeout
WAIT_TIMEOUT="--timeout=${WAIT_TIMEOUT:-10m0s}"
WAIT_OPT="--wait ${WAIT_TIMEOUT}"
if [ -z $RUN_CHART_TESTS ] && [ ! -z $SKIP_WAIT ]; then
  echo "WARNING: Skipping --wait!"
  WAIT_OPT=""
fi

## Namespace
NAMESPACE_OPT=""
if [ ! -z $NAMESPACE ]; then
  NAMESPACE_OPT="--namespace ${NAMESPACE}"
  if [ ! -z $CREATE_NAMESPACE ]; then
    NAMESPACE_OPT="${NAMESPACE_OPT} --create-namespace"
  fi
fi

## Image Option
if [ -z $IMAGE ]; then
  IMAGE=""
else
  IMAGE="--set image.repository=${IMAGE}"
fi

## Tag Option
if [ -z $TAG ]; then
  TAG="--set image.tag=local"
else
  TAG="--set image.tag=${TAG}"
fi

## Set release name
export RELEASE=${RELEASE:-metro2}

# Setup
## Get absolute path to helm-install.sh
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
## Get Project Dir path containing helm-install.sh
export PROJECT_DIR="$(dirname "$(realpath "$0")")"
## Set Default Args
DEFAULT_ARGS=""
## Source .env, if it exists
if [ -f .env ]; then
  source .env
fi

# Prerequisites
## Ensure helm is installed and available via PATH
if ! command -v helm &> /dev/null; then
  echo "Helm not found in PATH. Please install helm (brew install helm) or add it to PATH."
  exit 1
fi

## Build Dependency Charts
if [ ! -d ./helm/cfgov/charts ]; then
  echo "Building dependency charts..."
  helm repo add bitnami https://charts.bitnami.com/bitnami
  helm repo update
  helm dependency build ./helm/metro2
else
  if [ -z $SKIP_DEP_UPDATE ]; then
    helm dependency update ./helm/metro2
  fi
fi

# Generate Overrides
## Parse overrides list
if [ $# -eq 0 ]; then
  ARGS=${DEFAULT_ARGS}
else
  ARGS="$@"
fi

## Separate --set from files, substitute Environment Variables in override files
tempFiles=()
unset PENDING_SET
OVERRIDES=""
for i in $ARGS; do
  if [ ! -z $PENDING_SET ]; then
    OVERRIDES="${OVERRIDES} --set ${i}"
    unset PENDING_SET
  elif [ "${i}" == "--set" ]; then
    PENDING_SET=true
  else
    tempFile=$(mktemp)
    envsubst < ${i} > "$tempFile"
    OVERRIDES="$OVERRIDES -f $tempFile"
    tempFiles+=($tempFile)
  fi
done

# Execute
# install dbs for local releases
if [ "$TAG" == "--set image.tag=local" ]; then
  helm install metro2-db \
  --set auth.postgresPassword='cfpb' \
  --set auth.database='metro2-data' \
  bitnami/postgresql --set persistence.enabled=false

  helm install results-db \
  --set auth.postgresPassword='cfpb' \
  --set auth.database='metro2-results' \
  bitnami/postgresql --set persistence.enabled=false

  # wait for postgres to be in ready state
  kubectl wait --for=condition=ready \
  --all pods
fi

## Install/Upgrade cfgov release
helm upgrade --install ${WAIT_OPT} "${RELEASE}" \
${NAMESPACE_OPT} ${OVERRIDES} ${IMAGE} ${TAG} \
${PROJECT_DIR}/helm/metro2

# Add these in for local SSL.
#  --set ingress.tls[0].secretName="${RELEASE}-tls" \  # local SSL
#  --set ingress.tls[0].hosts[0]="${RELEASE}.localhost" \  # local SSL

## Run chart tests, if RUN_CHART_TESTS is set
if [ ! -z $RUN_CHART_TESTS ]; then
  echo "Running chart tests against ${RELEASE}..."
  helm test "${RELEASE}"
fi

# Cleanup
## Remove temp files
for i in "${tempFiles[@]}"; do
  rm "$i"
done
