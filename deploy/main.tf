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