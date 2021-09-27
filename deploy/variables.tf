variable "prefix" {
  default = "apideploy"
}

variable "project" {
  default = "app-api"
}

variable "contact" {
  default = "a1798286@student.adelaide.edu.au"
}

variable "db_username" {
  description = "Username for the RDS Postgres instance"
}

variable "db_password" {
  description = "Password for the RDS postgres instance"
}

variable "bastion_key_name" {
  default = "app-api-devops-bastion"
}

variable "ecr_image_api" {
  description = "ECR image for API"
  default     = "303205383285.dkr.ecr.us-east-1.amazonaws.com/recipe-app-api-devops:latest"
}

variable "ecr_image_proxy" {
  description = "ECR image for proxy"
  default     = "303205383285.dkr.ecr.us-east-1.amazonaws.com/recipe-app-api-proxy:latest"
}

variable "django_secret_key" {
  description = "Secret key for Django app"
}

variable "dns_zone_name" {
  description = "Domain name"
  default     = "cont7.link"
}

variable "subdomain" {
  description = "Subdomain per environment"
  type        = map(string)
  default = {
    production = "api"
    staging    = "api.staging"
    dev        = "api.dev"
  }
}
