import hashlib
import hmac
import base64
import github
from time import time

def verify_payload_signature(payload_body, secret_token, signature_header):
    """
    Verify that the payload was sent from GitHub. Return True if signature
    is verified successfully or False if signature cannot be verified

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        print("verify_signature: x-hub-signature-256 header is missing")
        return False
    
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body.encode('utf-8'), digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()

    if not hmac.compare_digest(expected_signature, signature_header):
        print("verify_signature: request signatures didn't match!")
        return False

    return True

def get_client_for_installation(app_id, private_key_base64, installation_id):
    """
    Github Applications can be installed on Organization or Personal accounts. We need to generate a github client 
    for a specific installation allowing us to talk to the resources (repos, PRs) for that installation
    """
    private_key = base64.b64decode(private_key_base64).decode()
    auth = github.Auth.AppAuth(app_id, private_key).get_installation_auth(installation_id)
    return github.Github(auth=auth)

def get_pr_file_diff(github_client, repository_name, pull_request_number):
    """
    Get the PR diff
    """
    repo = github_client.get_repo(repository_name)
    pull_request = repo.get_pull(pull_request_number)

    return pull_request.get_files()

def post_pr_comment(github_client, repository_name, pull_request_number, comment):
    """
    Post a generic comment on a pull request
    """
    repo = github_client.get_repo(repository_name)
    pr = repo.get_pull(pull_request_number)
    pr.create_issue_comment(comment)

def post_pr_comment_on_line(github_client, repository_name, pull_request_number, comment, commit_sha, path, line, suggestion):
    """
    Post a comment / suggestion on a pull request on a certain line
    """
    repo = github_client.get_repo(repository_name)
    pr = repo.get_pull(pull_request_number)
    commit = repo.get_commit(commit_sha)
    pr.create_review_comment(body=comment, commit=commit, path=path, line=line, as_suggestion=suggestion)
