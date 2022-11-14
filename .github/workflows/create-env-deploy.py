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


# Environment variables

# application slug
app_slug = "cd-test"

# environment slug
env_slug = "ci-cd"

# environment branch
branch = "cicdtest"

# api access token
load_dotenv()  # take environment variables from .env
api_token = os.getenv("API_TOKEN")


# Authentication headers
headers = {"Authorization": f"{api_token}"}


# Getting the application uuid

# params dictionary, the application slug
app_params = {"slug": app_slug}

# getting the application with the given app slug
app_response = requests.get(url=APP_URL, params=app_params, headers=headers)

# querying the application uuid from the single-item (0 index) list results
# .json() - converting the response to a json format to make it subscriptible
app_uuid = app_response.json()["results"][0]["uuid"]


# Getting the environemnt uuid
# if the environemnt does not exist, create it

# params dictionary, the application uuid
env_params = {"application": app_uuid}

# Listing the environments of the given application
env_response = requests.get(url=ENV_URL, params=env_params, headers=headers)

# Checking if the environemnt with the given slug exists
env_exist = False

# itereting through the list of the environemnts
for env in env_response.json()["results"]:
    if env["slug"] == env_slug:  # if environment slug exists
        env_exist = True  # the environment exists
        env_uuid = env["uuid"]  # getting the environemnt uuid

# if the environment does not exist
if env_exist is False:
    # Create the environment

    # defining required data for creating the environment
    env_data = {
        "application": app_uuid,  # the application uuid
        "slug": env_slug,  # the environment slug
        "branch": branch,  # the git branch
    }
    # making a post request, the API to create the environment
    env_response = requests.post(url=ENV_URL, data=env_data, headers=headers)
    env_uuid = env_response.json()["uuid"]  # getting the environment uuid


# Creating a deployment

# required data, the environment uuid
deploy_data = {"environment": env_uuid}

# making a post request, the API to trigger the deployment
deploy_post_response = requests.post(url=DEPLOY_URL, data=deploy_data, headers=headers)

# getting the deployment uuid
deploy_uuid = deploy_post_response.json()['uuid']

# defining GetDeployment URL from the deploy url and the deployment uuid
get_deployment_url = f"{DEPLOY_URL}{deploy_uuid}/"

# getting the deployment credentials
get_deployment_response = requests.get(url=get_deployment_url, headers=headers)


# Checking the status of the Deployment

# Loop until deployment is completed
while True:

    sleep(5)

    # getting the current deployment credentials
    get_deploy_response = requests.get(url=get_deployment_url, headers=headers)

    # current status of the deployment
    status = get_deploy_response.json()["status"]

    # success:  True - if deployment successfully completed;
    #           False - if deployment failed;
    #           None - if deployment is not yet completed
    success = get_deploy_response.json()["success"]

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
