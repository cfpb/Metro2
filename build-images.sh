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
docker build ./jobs/parseEvaluate/ -t "metro2_evaluator:$TAG"
echo "Building metro2_frontend:$TAG"
docker build ./front-end/ -t "metro2_frontend:$TAG"
echo "Building metro2_django:$TAG"
docker build ./django/ -t "metro2_django:$TAG"
