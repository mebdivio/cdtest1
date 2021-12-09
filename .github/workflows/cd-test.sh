#! /bin/bash

# From the Project SLUG, Jason Querying the API to get the APPLICATION UUID, removing the quotation mark
APPLICATION_UUID=$(curl https://api.divio.com/apps/v3/applications/\?slug\=$PROJECT_SLUG -H "Authorization: Token $API_TOKEN" | jq '.results[0].uuid'| tr -d '"')

# From the APPLICATION UUID, getting the ENVIRONMENT UUID
TEST_ENVIRONMENT_UUID=$(curl https://api.divio.com/apps/v3/environments/\?application\=$APPLICATION_UUID -H "Authorization: Token $API_TOKEN" | jq '.results[0].uuid'| tr -d '"')

# From the ENVIRONMENT UUID, getting the DEPLOYMENT UUID
TEST_DEPLOYMENT_UUID=$(curl -X POST --data "environment=$TEST_ENVIRONMENT_UUID" --header "Authorization: Token $API_TOKEN" https://api.divio.com/apps/v3/deployments/ | jq '.uuid'| tr -d '"')

# Loop until deployment is completed
while true; do
  sleep 1

# From the DEPLOYMENT UUID, querying and echoing the DEPLOYMENT credentials to a Jason file
  echo "$(curl https://api.divio.com/apps/v3/deployments/$TEST_DEPLOYMENT_UUID/ -H "Authorization: Token $API_TOKEN")" | jq '.' > deploy.json

# Querying the current status of the deployment from the Jason file and broadcasting it
  STATUS="$(jq '.status' deploy.json)"
  echo "Deployment ${STATUS}"

# Querying the current success status of the deployment from the Jason file
  SUCCESS="$(jq '.success' deploy.json)"

# Checking the current success status of the deployment 
# If success or failure report and exit, if not continue
  if [ $SUCCESS == true ]; then
    echo "Deployment has completed successfully"
    exit 0
    break
  elif [ $SUCCESS == false ]; then
    echo "Deployment has failed"
    exit 1
    break
  else
    continue
  fi
done