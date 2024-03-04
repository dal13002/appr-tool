terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "ai-powered-pr-review"
    key    = "terraform.tfstate"
    region = "us-east-2"
  }
}