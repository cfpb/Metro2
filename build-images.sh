#!/bin/sh


while getopts ":e:t:" opt; do
  case "$opt" in
    e)
      TARGET_ENV="$OPTARG"
      if [ "$TARGET_ENV" != "local" ] && [ "$TARGET_ENV" != "eks" ];
      then
        echo "-e flag must be 'local' or 'eks'"
        echo "Invalid flag value: $TARGET_ENV" 
        exit 1
      fi
      ;;
    t)
      TAG=$OPTARG
      ;;
    \?)
      echo "Valid flags: -e -t"
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

if [ -z "$TARGET_ENV" ]; then
  echo "Error: -e tag is required"
  exit 1
fi

if [ -z "$TAG" ]; then
  if [[ $TARGET_ENV == "eks" ]]; then
    echo "Error: -t tag is requried when -e 'eks' is specified"
    exit 1
  else
    echo "Waring: no -t tag specificed"
    echo "Images will be tagged with 'local'"
    TAG="local"
  fi
fi

if [[ $TARGET_ENV == "local" ]]; 
then
  TAG="local"
  echo "With TARGET_ENV set to 'local', images will be tagged with value 'local'"
  echo "Building metro2_evaluator:$TAG"
  docker build ./jobs/parseEvaluate/ -t "metro2_evaluator:$TAG"
  echo "Building metro2_frontend:$TAG"
  docker build ./front-end/ -t "metro2_frontend:$TAG"
  echo "Building metro2_django:$TAG"
  docker build ./django/ -t "metro2_django:$TAG" 
elif [[ $TARGET_ENV == "eks" ]];
then
  AWS_ACCOUNT_ID="795649122172"
  AWS_REGION="us-east-1"
  DOCKER_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com" 

  echo "Building metro2_evaluator:$TAG"
  ECR_REPO="cfpb/metro2/metro2-parse-evaluate"
  DOCKER_IMAGE=$DOCKER_REGISTRY/$ECR_REPO
  echo $DOCKER_IMAGE
  docker build ./jobs/parseEvaluate/ -t "$DOCKER_IMAGE:$TAG"

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
  echo "-e flag must be 'local' or 'eks'"  
  exit 1
fi