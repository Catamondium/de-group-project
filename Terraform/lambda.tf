resource "aws_lambda_function" "extraction_lambda" {
  function_name    = "${var.ingestion_lambda_name}lambda"
  role             = aws_iam_role.extraction_lambda_role.arn
  handler          = "extractor.lambda_handler"
  runtime          = "python3.11"
  s3_bucket        = "rannoch-s3-utility-bucket"
  s3_key           = "lambda-code/extraction_lambda.zip"
  layers           = ["arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:5"]
  source_code_hash = data.archive_file.lambda.output_base64sha256
  
  lifecycle {
    replace_triggered_by = [null_resource.sauce]
  }
  environment {
    variables = {
      S3_EXTRACT_BUCKET = aws_s3_bucket.rannoch-s3-ingestion-bucket.bucket
    }
  }
}

