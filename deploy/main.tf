terraform {
  backend "s3" {
    bucket         = "cont7-web-app-api-devops-tfstate"
    key            = "cont7-web-app-api.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "recipe-app-api-devops-tf-state-lock"
  }
}

// define the service provider, since update of service provider may break the code
provider "aws" {
  region  = "us-east-1"
  version = "~> 2.54.0"
}

// locals are ways that we can create dynamic variables inside Terraform <-> variables.tf
locals {
  prefix = "${var.prefix}-${terraform.workspace}"
  common_tags = {
    Environment = terraform.workspace
    Project     = var.project
    Owner       = var.contact
    ManagedBy   = "Terraform"
  }
}

