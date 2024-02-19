resource "aws_lambda_function" "extraction_lambda" {
    /*
    Defines an AWS Lambda function for data extraction.

    Args:
        function_name (str): The name of the Lambda function.
        role (str): The Amazon Resource Name (ARN) of the IAM role that the Lambda function can assume.
        handler (str): The name of the function (within your code) that Lambda calls to start execution.
        runtime (str): The runtime environment for the Lambda function.
        s3_bucket (str): The name of the Amazon S3 bucket that contains the deployment package.
        s3_key (str): The Amazon S3 object (the deployment package) key name.
        layers (list): List of ARNs of Lambda layers to attach to the Lambda function.
        source_code_hash (str): Base64-encoded representation of the SHA256 hash of the deployment package.
        memory_size (int): The amount of memory, in MB, that is allocated for the Lambda function.
        timeout (int): The function execution time (in seconds) after which Lambda terminates the function.

    Returns:
        None
    */
  function_name    = "${var.ingestion_lambda_name}lambda"
  role             = aws_iam_role.extraction_lambda_role.arn
  handler          = "extractor.lambda_handler"
  runtime          = "python3.11"
  s3_bucket        = "rannoch-s3-utility-bucket"
  s3_key           = "lambda-code/extraction_lambda.zip"
  layers           = ["arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:5"]
  source_code_hash = data.archive_file.lambda.output_base64sha256
  memory_size = 256
  timeout = 60
  
  lifecycle {
    replace_triggered_by = [null_resource.sauce]
  }
  environment {
    variables = {
      S3_EXTRACT_BUCKET = aws_s3_bucket.rannoch-s3-ingestion-bucket.bucket
      PGUSER = "${var.username}"
      PGPASSWORD = "${var.password}"
      PGHOST = "${var.host}"
      PGPORT = "${var.port}"
      PGDATABASE = "${var.database}"
      PG_LAST_UPDATED = "2000-01-01 00:00:00"
    }
  }
}
