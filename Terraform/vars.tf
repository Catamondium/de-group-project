# variables for everything
variable "utility_bucket" {
  type = string
  #default = "rannoch-s3-utility-bucket"
  default = "rannoch-transform-test-s3-utility-bucket"
}

#change this to keep bucket names separate
#also need to change remote tfvars name too
variable "environment" {
  type    = string
  default = "testing-"
}


variable "bucket_name" {
  type    = string
  default = "rannoch-testing-"
}

variable "ingestion_lambda_name" {
  type    = string
  default = "ingestion-testing-"
}

variable "transform_lambda_name" {
  type    = string
  default = "transform-testing-"
}

variable "extraction_lambda_name" {
  type    = string
  default = "extraction-testing-"
}
variable "loader_lambda_name" {
  type    = string
  default = "loader-testing-"
}

variable "username" {
  description = "username"
  type        = string
  sensitive   = true
}
variable "password" {
  description = "password"
  type        = string
  sensitive   = true
}
variable "host" {
  description = "host"
  type        = string
  sensitive   = true
}
variable "port" {
  description = "port"
  type        = number
  sensitive   = true
}
variable "database" {
  description = "database"
  type        = string
  sensitive   = true
}

# data warehouse
variable "OLAP_username" {
  description = "username"
  type        = string
  sensitive   = true
}
variable "OLAP_password" {
  description = "password"
  type        = string
  sensitive   = true
}
variable "OLAP_host" {
  description = "host"
  type        = string
  sensitive   = true
}
variable "OLAP_port" {
  description = "port"
  type        = string
  sensitive   = true
}
variable "OLAP_database" {
  description = "database"
  type        = string
  sensitive   = true
}
# variable "OLAP_schema" {
#     description = "schema"
#     type = string
#     sensitive = true
# }
