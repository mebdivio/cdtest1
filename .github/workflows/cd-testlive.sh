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
  
  if [ $success=='true' ] || [ $success=='false' ]; then
    echo "Success inside if is $success"
    if [ $success == 'true' ]; then 
      echo "Success inside second if for true is $success"
      echo "Deployment has completed successfully"
      exit 0
    else
      echo "Success inside second if 'else' expecting to be false is $success"
      echo "Deplyment has failed"
      exit 1
    fi
    break
  fi
done
