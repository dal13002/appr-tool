import json
import os

import utils
import gh
import oa

# Static Variables
GITHUB_APP_WEBHOOK_SECRET = os.environ['GITHUB_APP_WEBHOOK_SECRET']
GITHUB_APP_PRIVATE_KEY_BASE64 = os.environ['GITHUB_APP_PRIVATE_KEY_BASE64']
GITHUB_APP_ID = os.environ['GITHUB_APP_ID']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

def lambda_handler(event, context):
    print("Lambda triggered with event:", event)

    # Verify the request came from our Github App
    verified = gh.verify_payload_signature(
        event.get('body'), 
        GITHUB_APP_WEBHOOK_SECRET,
        event.get('headers', {}).get('x-hub-signature-256')
        )
    if not verified:
        fullComment = "Request signature could not be verified. The request must come from the Github Application"
        print(fullComment)
        return {
            "statusCode": 403,
            "body": json.dumps(fullComment)
        }

    # Pull out the variables that we need from the payload
    bodyJson = json.loads(event['body'])
    repositoryName = bodyJson.get('repository', {}).get('full_name') # dal13002/test
    pullRequestNumber = bodyJson.get('number') # 2
    gitEventType = event.get('headers', {}).get('x-github-event') # pull_request
    gitEventAction = bodyJson.get('action') # opened
    appInstallationID = bodyJson.get('installation', {}).get('id') # 47947445
    commitSha = bodyJson.get('pull_request', {}).get('head', {}).get('sha') # 5c8ca1d660b72684d13c98bcc0cbbf39ceb27f3a
    pullRequestTitle = bodyJson.get('pull_request', {}).get('title') # Quick Application for testing
    pullRequestLabels = bodyJson.get('pull_request', {}).get('labels', []) # ['appr.disabled']

    # Validate the event payload
    validEvent = utils.validate_event(
        repositoryName, 
        pullRequestNumber, 
        gitEventType, 
        gitEventAction, 
        appInstallationID, 
        commitSha, 
        pullRequestTitle,
        pullRequestLabels
    )
    if not validEvent:
        fullComment = "Invalid Input. Application can only be triggered from Github App when PR is opened"
        print(fullComment)
        return {
            "statusCode": 422,
            "body": json.dumps(fullComment)
        }

    # Configure tool based on labels on the pull request
    ghClient = gh.get_client_for_installation(GITHUB_APP_ID, GITHUB_APP_PRIVATE_KEY_BASE64, appInstallationID)
    for label in pullRequestLabels:
        if label['name'] == "appr.disabled":
            fullComment = "Pull Request contains label `appr.disabled`. Not running AI Powered Pull Request Tool"
            print(fullComment)
            gh.post_pr_comment(ghClient, repositoryName, pullRequestNumber, fullComment)
            return {
                "statusCode": 200,
                "body": json.dumps(fullComment)
            }

    # Analyze pull request changes per file using OpenAI. Update pull request based on recommendations
    gitDiffs = gh.get_pr_file_diff(ghClient, repositoryName, pullRequestNumber)
    oaClient = oa.get_client(OPENAI_API_KEY)
    for file in gitDiffs:
        feedback = json.loads(oa.analyze_file(oaClient, pullRequestTitle, file.patch))

        for comment in feedback['comments']:
            try:
                if comment['line'] == None:
                    fullComment = f"> Comment is in respect to file {file.filename}\n\n" + comment['comment']
                    gh.post_pr_comment(ghClient, repositoryName, pullRequestNumber, fullComment)
                else:
                    gh.post_pr_comment_on_line(ghClient, repositoryName, pullRequestNumber, comment['comment'], commitSha, file.filename, comment['line'], False)
            except Exception as e:
                print(f"Error making comment for line {comment['line']} with comment {comment['comment']}: ", e)

        for code_change in feedback['code_changes']:
            try:
                gh.post_pr_comment_on_line(ghClient, repositoryName, pullRequestNumber, code_change['change'], commitSha, file.filename, code_change['line'], True)
            except Exception as e:
                print(f"Error making code change suggestion for line {code_change['line']} and suggestion {code_change['change']}: ", e)


    # Respond to the webhook. Github stores the responses which is useful for debugging
    successfulMessage = "PR analysis completed. Comments and suggestion successfully added."
    print(successfulMessage)
    return {
        "statusCode": 200,
        "body": json.dumps(successfulMessage)
    }