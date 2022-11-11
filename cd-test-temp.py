#!/usr/bin/python

import os
import requests
from time import sleep
from dotenv import load_dotenv  # to read env vars from .env

# API-endpoints

# for applications
APP_URL = "https://api.divio.com/apps/v3/applications/"

# for environments
ENV_URL = "https://api.divio.com/apps/v3/environments/"

# for deployments
DEPLOY_URL = "https://api.divio.com/apps/v3/deployments/"

# Defining Environment variables

# application slug
app_slug = "cd-test"

# api access token
load_dotenv()  # take environment variables from .env
API_TOKEN = os.getenv("API_TOKEN")

# defining authentication headers
headers = {"Authorization": f"{API_TOKEN}"}

# defining a params dictionary, the application slug,
# in querying for the application
app_params = {"slug": app_slug}

# requesting the API to get the application using the params,
# the application slug
app_response = requests.get(url=APP_URL, params=app_params, headers=headers)

# The application response contains
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
app_uuid = app_response.json()["results"][0]["uuid"]

# defining a params dictionary of application uuid,
# in querying for environments
env_params = {"application": app_uuid}

# making a request, the API to get the list of environments using the app uuid
env_response = requests.get(url=ENV_URL, params=env_params, headers=headers)

# The environemnt response contains
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
    if env["slug"] == "test":
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


import pdb

pdb.set_trace()
# .json()['results'][0]['success']
# .json() - converting the response to a json format
# to make it subscriptible - an object that can contain other objects like list
# 'results'][0]['success'] - getting the success state of the deployment
# [0] - the current(first) deployment from the resulting list of deployments

# The Test deploy response contains
# response = {"count": #####,        - count: number of deployments
#             "next":next_page_no.,  - next/previous displays an integer
#                                      depends on the number of deployments
#             "previous":prev_p_no., - next: displys the next page number and
#                                      previous: displays the previous page no.
#             "results":[            - results: the response
#                                   the required information to be queried from
#                 {                  - {}: list of the deployment credentials
#                 "uuid":            - uuid: unique identifier for a deployment
#                 "environemnt":     - environemnt: the environemnt uuid
#                 "region":          - region: the region uuid
#                 "started_at":      - started_at: time when deployment started
#                 "ended_at":        - ended_at: time when deployment finished
#                                       None during deployment
#                 "status":          - status: the status of the deployment
#                 "is_usable":       - is_usable: is the deployment ready
#                 "success"          - success: None / True / False depends on
#                                      the success state of the deployment
#                 }]
#          }


# Loop until deployment is completed
while True:

    sleep(3)

    # Continuously making a request, the API to get
    # the current deployment credentials
    get_deployment_response = requests.get(url=get_deployment_url, headers=headers)
    
    success = get_deployment_response.json()['success']
    status = get_deployment_response.json()['status']
    # status = requests.get(
    #     url=DEPLOY_URL, params=TEST_DEPLOY_PARAMS, headers=headers
    # ).json()["results"][0]["status"]

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

# - below - to be used in another file: deployment by creating an environemnt

# # Creating an environment

# # defining environment slug
# ENV_SLUG = "ci-cd"

# # defining a data dictionary of required credentials
# # for creating the environment
# data = {
#     "application": "APP_UUID",  # the application uuid
#     "slug": "ENV_SLUG",  # the environment slug
#     "branch": "develop",  # the git branch for the environemnt
# }
