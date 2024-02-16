resource "aws_s3_bucket" "rannoch-s3-ingestion-bucket"{
    bucket = "${var.bucket_name}ingestion-bucket"
    force_destroy = true
}

resource "aws_s3_object" "lambda_code" {
  bucket = "rannoch-s3-utility-bucket-test"
  key = "lambda-code/extraction_lambda.zip"
  source = "${path.module}/../extraction_lambda.zip"

  lifecycle {
    replace_triggered_by = [null_resource.sauce]
  }
}

resource "aws_s3_bucket_versioning" "versioning_example" {
  bucket = aws_s3_bucket.rannoch-s3-ingestion-bucket.id
  versioning_configuration {
    status = "Enabled"
    #disabled by default
  }
}

# this will not run if versioning is disabled
# have to do another terraform apply to ensure retention
resource "aws_s3_bucket_object_lock_configuration" "example" {
  bucket = aws_s3_bucket.rannoch-s3-ingestion-bucket.id

  rule {
    default_retention {
      mode = "GOVERNANCE"
      days = 5
    }
  }
}