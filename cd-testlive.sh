#! /bin/bash

LIVE_DEPLOYMENT_ID="$(curl -X POST --data "environment=$LIVE_ENVIRONMENT_ID" --header "Authorization: Token $API_TOKEN" https://api.divio.com/apps/v3/deployments/ | jq '.uuid')"
echo "The deployment id is: $LIVE_DEPLOYMENT_ID"

while true; do 
  sleep 1
  DEPLOY="$(curl https://api.divio.com/apps/v3/deployments/$LIVE_DEPLOYMENT_ID/ -H "Authorization: Token $API_TOKEN")"
  echo "${DEPLOY}" | jq '.' > deploy.json
  status="$(jq '.status' deploy.json)"
  echo "${status} on progress"
  success="$(jq '.success' deploy.json)"
  echo "Success is ${success}"
  if [ $success == 'true' ]; then 
      echo "Success for true is $success"
      echo "Deployment has completed successfully"
      exit 0
      break
  elif [ $success == 'fals' ]; then 
      echo "Success for false is $success"
      echo "Deplyment has failed"
      exit 1
      break
  fi
done
 