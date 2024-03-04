def validate_event(repository_name, pull_request_number, git_event_type, git_event_action, app_installation_id, commit_sha, pull_request_title, pull_request_labels):
    """
    Validate input for the reqeust that invoked lambda
    """
    print(f"""Running event validation
    repository_name: {repository_name}
    pull_request_number: {pull_request_number}
    git_event_type: {git_event_type}
    git_event_action: {git_event_action}
    app_installation_id: {app_installation_id}
    commit_sha: {commit_sha}
    pull_request_title: {pull_request_title}
    pull_request_labels: {pull_request_labels}
    """)
    
    valid = True

    if repository_name is None:
        print("event does not have repository_name")
        valid = False

    if pull_request_number is None:
        print("event does not have pull_request_number")
        valid = False

    if git_event_type != "pull_request":
        print("event does not have git_event_type of type pull request")
        valid = False

    if git_event_action != "opened":
        print("event does not have git_event_action of type opened")
        valid = False

    if app_installation_id is None:
        print("event does not have app_installation_id")
        valid = False

    if commit_sha is None:
        print("event does not have commit_sha")
        valid = False

    if pull_request_title is None:
        print("event does not have pull_request_title")
        valid = False

    return valid