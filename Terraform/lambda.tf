resource "aws_lambda_function" "s3_file_reader" {
  function_name = "${var.ingestion_lambda_name}lambda"
  role          = aws_iam_role.extraction_lambda_role.arn
  handler       = "extractor.lambda_handler"
  runtime       = "python3.11"
  s3_bucket     = "rannoch-s3-utility-bucket"
  s3_key        = "lambda-code/extraction_lambda.zip"
  layers        = ["arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:5"]
  environment {
    variables = {
      S3_EXTRACT_BUCKET = aws_s3_bucket.rannoch-s3-ingestion-bucket.bucket
    }
  }
}

