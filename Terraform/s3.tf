resource "aws_s3_bucket" "rannoch-s3-ingestion-bucket"{
    /*
    Creates an Amazon S3 bucket for data ingestion.

    Args:
        bucket (str): The name of the S3 bucket.
        force_destroy (bool): A boolean flag indicating whether all objects should be deleted from the bucket before deleting the bucket.

    Returns:
        None
    */
    bucket = "${var.bucket_name}ingestion-bucket"
    force_destroy = true
}
resource "aws_s3_bucket" "rannoch-s3-processed-data-bucket"{
    /*
    Creates an Amazon S3 bucket for data ingestion.

    Args:
        bucket (str): The name of the S3 bucket.
        force_destroy (bool): A boolean flag indicating whether all objects should be deleted from the bucket before deleting the bucket.

    Returns:
        None
    */
    bucket = "${var.bucket_name}processed-data-bucket"
    force_destroy = true
}

resource "aws_s3_object" "lambda_code" {
    /*
    Creates an Amazon S3 bucket for data ingestion.

    Args:
        bucket (str): The name of the S3 bucket.
        force_destroy (bool): A boolean flag indicating whether all objects should be deleted from the bucket before deleting the bucket.

    Returns:
        None
    */
  bucket = "rannoch-s3-utility-bucket"
  key = "lambda-code/extraction_lambda.zip"
  source = "${path.module}/../extraction_lambda.zip"

  lifecycle {
    replace_triggered_by = [null_resource.extraction]
  }
}
resource "aws_s3_object" "transformation_lambda_code" {
    /*
    Creates an Amazon S3 bucket for data ingestion.

    Args:
        bucket (str): The name of the S3 bucket.
        force_destroy (bool): A boolean flag indicating whether all objects should be deleted from the bucket before deleting the bucket.

    Returns:
        None
    */
  bucket = "rannoch-s3-utility-bucket"
  key = "lambda-code/transformation_lambda.zip"
  source = "${path.module}/../transformation_lambda.zip"

  lifecycle {
    replace_triggered_by = [null_resource.extraction]
  }
}

resource "aws_s3_bucket_versioning" "versioning_example" {
   /*
   Enables versioning for an Amazon S3 bucket.

    Args:
        bucket (str): The ID of the S3 bucket for which versioning is enabled.

    Returns:
        None
   */ 
  bucket = aws_s3_bucket.rannoch-s3-ingestion-bucket.id
  versioning_configuration {
    status = "Enabled"
    #disabled by default
  }
}
resource "aws_s3_bucket_versioning" "versioning_example" {
   /*
   Enables versioning for an Amazon S3 bucket.

    Args:
        bucket (str): The ID of the S3 bucket for which versioning is enabled.

    Returns:
        None
   */ 
  bucket = aws_s3_bucket.rannoch-s3-processed-data-bucket.id
  versioning_configuration {
    status = "Enabled"
    #disabled by default
  }
}

# this will not run if versioning is disabled
# have to do another terraform apply to ensure retention
resource "aws_s3_bucket_object_lock_configuration" "example" {
    /*
    Configures object lock for an Amazon S3 bucket.

    Args:
        bucket (str): The ID of the S3 bucket for which object lock is configured.

    Returns:
        None
    */
  bucket = aws_s3_bucket.rannoch-s3-ingestion-bucket.id

  rule {
    default_retention {
      mode = "GOVERNANCE"
      days = 5
    }
  }
}
resource "aws_s3_bucket_object_lock_configuration" "example" {
    /*
    Configures object lock for an Amazon S3 bucket.

    Args:
        bucket (str): The ID of the S3 bucket for which object lock is configured.

    Returns:
        None
    */
  bucket = aws_s3_bucket.rannoch-s3-processed-data-bucket.id

  rule {
    default_retention {
      mode = "GOVERNANCE"
      days = 5
    }
  }
}