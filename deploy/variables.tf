variable "prefix" {
  default = "craa"
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
