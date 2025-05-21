variable "aws_region" {
  description = "AWS Region where infrastructure is deployed"
  type        = string
}

variable "environment" {
  description = "Deployment stage / environment. Like Dev, Prod, Test"
  type        = string
}

variable "lambda_tag" {
  type    = string
  default = "latest"
}

variable "log_retention" {
  type    = number
  default = 14
}

variable "app_name" {
  type = string
}

variable "runtime" {
  type = string
}

variable "arch" {
  type = string
}

variable "handler" {
  type = string
}

variable "memory_size" {
  type    = number
  default = 256
}

variable "timeout" {
  type    = number
  default = 5
}

variable "provider_bucket_name" {
  description = "Deployment bucket. Infra tfstate will be saved in this bucket."
  type        = string
}

variable "allowed_domain_patterns" {
  type = string
}
