#!/bin/sh

TAG=$1
if [ -z "$TAG" ]; then
  TAG="local"
fi

case "$TAG" in
  "local")
    TARGET="dev"
    ;;
  "prod")
    TARGET="prod"
    ;;
  *)
    echo "Tag must be 'local' or 'prod'"
    exit 2
esac

echo "Building metro2_evaluator:$TAG"
docker build . -t "metro2_evaluator:$TAG"
echo "Building metro2_frontend:$TAG"
docker build ./front-end/ -t "metro2_frontend:$TAG"
