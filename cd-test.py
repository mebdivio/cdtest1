#!/usr/bin/env python3

import os
import requests
from time import sleep
from dotenv import load_dotenv  # to read env vars from .env

# API-endpoints

# for listing and creating applications
APP_URL = "https://api.divio.com/apps/v3/applications/"

# for listing and creating environments
ENV_URL = "https://api.divio.com/apps/v3/environments/"

# for listing and creating deployments
DEPLOY_URL = "https://api.divio.com/apps/v3/deployments/"

# Defining Environment variables

# application slug
app_slug = "cd-test"

# environment slug
env_slug = "test"

# api access token
load_dotenv()  # take environment variables from .env
api_token = os.getenv("API_TOKEN")

# defining authentication headers
headers = {"Authorization": f"{api_token}"}

# defining a params dictionary, the application slug,
# in querying for the application
app_params = {"slug": app_slug}

# requesting the API to get the application using the params,
# the application slug
app_response = requests.get(url=APP_URL, params=app_params, headers=headers)

# The application response credentials
# response = {"count": 1,       - count - one application for a specific slug
#             "next":null,      - next display - none - single application
#             "previous":null,  - previous display - none - single application
#             "results":        - results - the response,
#                                 the required information to be queried from
#                 [             - [] - a single-item list per application
#                 {"uuid":      - uuid - unique identifier for the application
#                 ...}
#                 ]}

# Extracting data in a json format
# from the results of a single-item list (0 index)
# querying the application uuid
# .json() - converting the response to a json format to make it subscriptible
app_uuid = app_response.json()["results"][0]["uuid"]

# defining a params dictionary of application uuid,
# in querying for environments
env_params = {"application": app_uuid}

# making a request, the API to get the list of environments using the app uuid
env_response = requests.get(url=ENV_URL, params=env_params, headers=headers)

# The environemnt response credentials
# response = {"count": 2,       - count - number of environments
#             "next":null,      - next/previos display - none
#             "previous":null,  - limited environments per application
#             "results":        - results - the response
#                                 the required information to be queried from
#                 {             - {} - a dictionary list of the environments
#                 "uuid":       - uuid - a unique identifier for an environment
#                 ...}
#             }

# Getting the uuid of a specific environment
# itereting through the list of environemnts

for env in env_response.json()["results"]:
    # getting the uuid of the Test environment from its slug (test)
    if env["slug"] == env_slug:
        test_env_uuid = env["uuid"]

# defining a required data, the test environment uuid, for deployment
test_deploy_data = {"environment": test_env_uuid}

# making a post request, the API to trigger the deployment of
# the Test environment using the Test environment uuid data
test_deploy_post_response = requests.post(
    url=DEPLOY_URL, data=test_deploy_data, headers=headers
)

# Getting the Test deployment uuid
test_deploy_uuid = test_deploy_post_response.json()["uuid"]

# defining GetDeployment URL using the Test deployment uuid,
# in querying for deployment credentials
get_deployment_url = f"{DEPLOY_URL}{test_deploy_uuid}/"

# making a request, the API to get the deployment credentials
get_deployment_response = requests.get(url=get_deployment_url, headers=headers)


# Loop until deployment is completed
while True:

    sleep(5)

    # making a request, the API to get the deployment credentials
    get_deployment_response = requests.get(
        url=get_deployment_url, headers=headers
    ).json()

    # The deployment crentials

    # The current status of the deployment
    status = get_deployment_response["status"]

    # success:  True - if deployment successfully completed;
    #           False - if deployment failed;
    #           None - if deployment is not yet completed
    success = get_deployment_response["success"]

    # Checking the current success status of the deployment
    # If success or failure, report and exit,
    # if not report the status and continue
    if success is True:
        print("Deployment has completed successfully")
        break
    elif success is False:
        print("Deployment has failed, please check the Deployment logs")
        break
    else:
        print("Deployment", status)
        continue
