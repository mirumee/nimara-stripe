provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      component   = var.app_name
      Environment = var.environment
    }
  }
}

terraform {
  required_version = "1.9.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.91.0"
    }
  }
  backend "s3" {
    bucket  = var.provider_bucket_name
    key     = "${var.environment}-${var.app_name}-state.tfstate"
    region  = var.aws_region
    encrypt = true
  }
}
