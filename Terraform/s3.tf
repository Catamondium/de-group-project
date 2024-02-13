resource "aws_s3_bucket" "rannoch-s3-ingestion-bucket"{
    bucket = "${var.bucket_name}ingestion-bucket"
}

resource "aws_s3_object" "lambda_code" {
  bucket = "rannoch-s3-utility-bucket"
  key = "lambda-code/extraction_lambda.zip"
  source = "${path.module}/../extraction_lambda.zip"
}