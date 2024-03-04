from openai import OpenAI

def get_client(api_key):
    """
    Returns OpenAI Client Instance
    """
    return OpenAI(api_key=api_key)


def analyze_file(client, pr_title, patch):
    """
    API call to OpenAI to generate meaningful insights for a file in a pull request.
    """

    systemContext = """
    You are a code reviewer for pull requests. You will understand the context and impact of the pull request on the overall codebase.
    You will be given the pull request title followed by the git diff in unified-diff format for a single file of the pull request. 
    It is important to keep track of the line numbers when parsing the code patch since you will return comments and suggestions for specific line numbers.
    You will need to generate:
    1. Clear, concise, and actionable comments that provide constructive feedback to the developer
    2. Explicit code change you would make on a certain line of the code. This should return only the exact code you would suggest and only for code that has been added (not removed). 
    The changes should not be multiple lines long (ie do not use /n) as they should be per line

    The return must be in this json format:
    { 
        "comments": [
            {
              "line": <line number>,
              "comment": <comment>
            }
        ]
        "code_changes": [
            {
              "line": <line number>,
              "change": <explicit code change>
            }
        ]
    }

    The line number in the comments section can be `null` if it is a generic comment. If there is no change needed, return
    the same json format but the comments array and code_changes array will be empty
    """

    userContent = f"""
    The title is: {pr_title}
    The patch is the following:
    {patch}
    """

    completion = client.chat.completions.create(
        messages = [
            {
                "role": "system",
                "content":  systemContext
            },
            {
                "role": "user",
                "content": userContent
            }
        ],
        model = "gpt-4-1106-preview",
        max_tokens = 4000,
        response_format={ "type": "json_object" }
    )

    return completion.choices[0].message.content