#! /bin/bash
APPLICATION_ID=$(curl https://api.divio.com/apps/v3/applications/\?slug\=$PROJECT_SLUG -H "Authorization: Token $API_TOKEN" | jq '.results[0].uuid'| tr -d '"')
TEST_ENVIRONMENT_ID=$(curl https://api.divio.com/apps/v3/environments/\?application\=$APPLICATION_ID -H "Authorization: Token $API_TOKEN" | jq '.results[0].uuid'| tr -d '"')
TEST_DEPLOYMENT_ID=$(curl -X POST --data "environment=$TEST_ENVIRONMENT_ID" --header "Authorization: Token $API_TOKEN" https://api.divio.com/apps/v3/deployments/ | jq '.uuid'| tr -d '"')

while true; do 
  sleep 1
  echo "$(curl https://api.divio.com/apps/v3/deployments/$TEST_DEPLOYMENT_ID/ -H "Authorization: Token $API_TOKEN")" | jq '.' > deploy.json
  STATUS="$(jq '.status' deploy.json)"
  echo "Deployment ${STATUS}"
  SUCCESS="$(jq '.success' deploy.json)"
  if [ $SUCCESS == true ]; then 
    echo "Deployment has completed successfully"
    break
  elif [ $SUCCESS == false ]; then  
    echo "Deplyment has failed"
    break
  else
    continue
  fi
done
 