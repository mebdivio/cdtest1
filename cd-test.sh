# #! /bin/bash
# echo "The Project slug is: ${PROJECT_SLUG}"
# export APPLICATION_ID=$(curl https://api.divio.com/apps/v3/applications/\?slug\=$PROJECT_SLUG -H "Authorization: Token $API_TOKEN" | jq '.results.uuid'| tr -d '"')

# echo "The APPLICATION_ID is: ${PROJECT_SLUG}"
# export TEST_ENVIRONMENT_ID=$(curl -X POST --data "environment=$TEST_ENVIRONMENT_ID" --header "Authorization: Token $API_TOKEN" https://api.divio.com/apps/v3/deployments/ | jq '.result.uuid'| tr -d '"')


export TEST_DEPLOYMENT_ID=$(curl -X POST --data "environment=$TEST_ENVIRONMENT_ID" --header "Authorization: Token $API_TOKEN" https://api.divio.com/apps/v3/deployments/ | jq '.uuid'| tr -d '"')
echo "The deployment is: ${TEST_DEPLOYMENT_ID}"

while true; do 
  sleep 1
  echo "The deployment id is: ${TEST_DEPLOYMENT_ID}"
  export DEPLOY=$(curl https://api.divio.com/apps/v3/deployments/$TEST_DEPLOYMENT_ID/ -H "Authorization: Token $API_TOKEN")
  echo "${DEPLOY}" | jq '.' > deploy.json
  STATUS="$(jq '.status' deploy.json)"
  echo "${STATUS} in progress"
  SUCCESS="$(jq '.success' deploy.json)"
  echo "Success is ${SUCCESS}."
  if [ $SUCCESS == true ]; then 
    echo "Deployment has completed successfully"
    exit 0
    break
  elif [ $SUCCESS == false ]; then  
    echo "Deplyment has failed"
    exit 1
    break
  else
    echo "Deplyment has not yet finished"
  fi
done
 