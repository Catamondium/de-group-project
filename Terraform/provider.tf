provider "aws" {
    region = "eu-west-2"
}

terraform {
    backend "s3" {
        bucket = "rannoch-s3-utility-bucket-test"
        key = "utility/tfstate"
        region = "eu-west-2"
    }
    required_providers {
        aws = {
            source = "hashicorp/aws"
        }
    }
}