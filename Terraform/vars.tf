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