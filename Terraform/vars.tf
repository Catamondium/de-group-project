# variables for everything

variable "bucket_name" {
    type = string
    default = "rannoch-"
}

variable "ingestion_lambda_name" {
    type = string
    default = "ingestion-"
}

variable "transform_lambda_name" {
    type = string
    default = "transform-"
}

variable "extraction_lambda_name" {
    type = string
    default = "extraction-"
}

variable "username" {
    description = "username"
    type = string
    sensitive = true
}
variable "password" {
    description = "password"
    type = string
    sensitive = true
}
variable "host" {
    description = "host"
    type = string
    sensitive = true
}
variable "port" {
    description = "port"
    type = number
    sensitive = true
}
variable "database" {
    description = "database"
    type = string
    sensitive = true
}