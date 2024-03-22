#!/bin/sh

HELP_TEXT_1="Valid flags:"
HELP_TEXT_2="  -e  environment | Required. Valid values: 'eks' or 'local'"
HELP_TEXT_3="  -t  tag         | Required when environment=eks. Ignored when environment=local"
HELP_TEXT="$HELP_TEXT_1\n$HELP_TEXT_2\n$HELP_TEXT_3\n"

while getopts ":e:t:" opt; do
  case "$opt" in
    e)
      TARGET_ENV="$OPTARG"
      if [ "$TARGET_ENV" != "local" ] && [ "$TARGET_ENV" != "eks" ]; then
        echo $HELP_TEXT
        echo "Invalid value for -e flag: $TARGET_ENV"
        exit 1
      fi
      ;;
    t)
      TAG=$OPTARG
      ;;
    \?)
      echo $HELP_TEXT
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo $HELP_TEXT
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

if [ -z "$TARGET_ENV" ]; then
  echo $HELP_TEXT
  echo "Error: -e tag is required"
  exit 1
fi

if [ -z "$TAG" ]; then
  if [[ $TARGET_ENV == "eks" ]]; then
    echo $HELP_TEXT
    echo "Error: -t tag is requried when -e 'eks' is specified"
    exit 1
  fi
fi

if [[ $TARGET_ENV == "eks" ]]; then
  AWS_ACCOUNT_ID="795649122172"
  AWS_REGION="us-east-1"
  DOCKER_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com" 

  echo "Building metro2_frontend:$TAG"
  ECR_REPO="cfpb/metro2/metro2-frontend"
  DOCKER_IMAGE=$DOCKER_REGISTRY/$ECR_REPO
  echo $DOCKER_IMAGE
  docker build ./front-end/ -t "$DOCKER_IMAGE:$TAG"

  echo "Building metro2_django:$TAG"
  ECR_REPO="cfpb/metro2/metro2-django"
  DOCKER_IMAGE=$DOCKER_REGISTRY/$ECR_REPO
  echo $DOCKER_IMAGE
  docker build ./django/ -t "$DOCKER_IMAGE:$TAG"
else
  # If TARGET_ENV isn't eks, it must be local
  TAG="local"
  echo "With TARGET_ENV set to 'local', images will be tagged with value 'local'"
  echo "Building metro2_frontend:$TAG"
  docker build ./front-end/ -t "metro2_frontend:$TAG"
  echo "Building metro2_django:$TAG"
  docker build ./django/ -t "metro2_django:$TAG"
fi
