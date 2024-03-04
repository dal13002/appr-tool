# Overview
This codebase is to deploy the lambda function which will do the automated AI PR review. This function, when invoked, will send a request to OpenAI and get feedback. Then it will write that feedback directly on the PR. The source code can be found in `lambda/src` folder

# How to deploy
1. Set the Variables
```
# AWS
export AWS_ACCESS_KEY_ID="anaccesskey"
export AWS_SECRET_ACCESS_KEY="asecretkey"
export AWS_REGION="us-east-2"

# Github
export TF_VAR_GITHUB_APP_WEBHOOK_SECRET="secretkey"
export TF_VAR_GITHUB_APP_ID="id"
export TF_VAR_GITHUB_APP_PRIVATE_KEY_BASE64="base64key"

# OpenAI
export TF_VAR_OPENAI_API_KEY="secretkey"
```
2. Deploy terraform
```
terraform init
terraform apply
```