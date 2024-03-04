module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name              = "ai-powered-pr-review"
  description                = "Function to get output from OpenAI and write feedback on PR"
  handler                    = "main.lambda_handler"
  runtime                    = "python3.9"
  create_lambda_function_url = true
  architectures              = ["x86_64"]
  layers = [
    module.lambda_layer_s3.lambda_layer_arn
  ]

  # reserved_concurrent_executions = 1
  timeout = 300

  environment_variables = {
    GITHUB_APP_WEBHOOK_SECRET     = var.GITHUB_APP_WEBHOOK_SECRET
    GITHUB_APP_PRIVATE_KEY_BASE64 = var.GITHUB_APP_PRIVATE_KEY_BASE64
    GITHUB_APP_ID                 = var.GITHUB_APP_ID
    OPENAI_API_KEY                = var.OPENAI_API_KEY
  }

  source_path = "./lambda/src"
}


resource "aws_s3_bucket" "lambda_layer_s3" {
  bucket = "al-powered-lambda-layers"
}

module "lambda_layer_s3" {
  source = "terraform-aws-modules/lambda/aws"

  create_layer = true

  layer_name          = "ai-powered-pr-review-dependencies"
  description         = "External packages needed to run ai-powered-pr-review lambda"
  compatible_runtimes = ["python3.9"]

  source_path = "./lambda/layer"

  store_on_s3 = true
  s3_bucket   = aws_s3_bucket.lambda_layer_s3.id
}
