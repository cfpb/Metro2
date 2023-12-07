#!/bin/sh


while getopts ":e:" opt; do
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
    \?)
      echo "Valid flags: -e"
      echo "Invalid option: -$OPTARG"
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument."
      exit 1
      ;;
  esac
done

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
  TAG="latest"

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