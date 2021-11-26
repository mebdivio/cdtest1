#! /bin/bash

export TEST_DEPLOYMENT_ID=$(curl -X POST --data "environment=$TEST_ENVIRONMENT_ID" --header "Authorization: Token $API_TOKEN" https://api.divio.com/apps/v3/deployments/ | jq '.uuid')
echo "The deployment is: ${TEST_DEPLOYMENT_ID}"
# echo "${DEPLOYMENT}" | jq '.' > deploy.json
# export TEST_ENVIRONMENT_ID="$(jq '.uuid' deploy.json)"


# export TEST_DEPLOYMENT_ID=$(curl -X POST --data "environment=$TEST_ENVIRONMENT_ID" --header "Authorization: Token $API_TOKEN" https://api.divio.com/apps/v3/deployments/ | jq '.uuid')
# echo "The deployment id is: ${TEST_DEPLOYMENT_ID}"

while true; do 
  sleep 1
  echo "The deployment id is: ${TEST_DEPLOYMENT_ID}"
  export DEPLOY=$(curl https://api.divio.com/apps/v3/deployments/$TEST_DEPLOYMENT_ID/ -H "Authorization: Token $API_TOKEN")
  echo "${DEPLOY}"
  export STATUS=$(curl https://api.divio.com/apps/v3/deployments/$TEST_DEPLOYMENT_ID/ -H "Authorization: Token $API_TOKEN"| jq '.status')
  echo "Status is ${STATUS}."
  export SUCCESS=$(curl https://api.divio.com/apps/v3/deployments/$TEST_DEPLOYMENT_ID/ -H "Authorization: Token $API_TOKEN"| jq '.success')
  # # echo "${DEPLOY}"
  # # echo "${DEPLOY}" | jq '.' > deploy.json
  # # status="$(jq '.status' deploy.json)"
  # echo "${status} in progress"
  # success="$(jq '.success' deploy.json)"
  echo "Success is ${SUCCESS}."
  if [ $SUCCESS == 'true' ]; then 
    echo "Deployment has completed successfully"
    exit 0
    break
  elif [ $SUCCESS == 'false' ]; then  
    echo "Deplyment has failed"
    exit 1
    break
  else
    echo "Deplyment has not yet finished"
  fi
done
 