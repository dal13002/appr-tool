variable "GITHUB_APP_WEBHOOK_SECRET" {
  type        = string
  description = "Github App Webhook Secret to verify payload"
  sensitive   = true
}

variable "GITHUB_APP_PRIVATE_KEY_BASE64" {
  type        = string
  description = "Github App private key in base64 encoded format, which is used to make requests to github as the application"
  sensitive   = true
}

variable "GITHUB_APP_ID" {
  type        = string
  description = "Github App ID"
}

variable "OPENAI_API_KEY" {
  type        = string
  description = "OpenAI API Key"
  sensitive   = true
}