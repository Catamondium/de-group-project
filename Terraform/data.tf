data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "archive_file" "lambda" {
  /*
    Creates an archive file containing the Lambda function code and dependencies.

    Args:
        type (str): The type of archive file to create (e.g., "zip").
        source_file (str): The path to the main source file or directory to include in the archive.
        output_path (str): The path where the archive file will be generated.

    Returns:
        None
    */
  type        = "zip"
  source_file = "${path.module}/../src/extractor.py"
  output_path = "${path.module}/../extraction_lambda.zip"

  depends_on = [null_resource.extraction]
}
data "archive_file" "transformation_lambda" {
  /*
    Creates an archive file containing the Lambda function code and dependencies.

    Args:
        type (str): The type of archive file to create (e.g., "zip").
        source_file (str): The path to the main source file or directory to include in the archive.
        output_path (str): The path where the archive file will be generated.

    Returns:
        None
    */
  type        = "zip"
  source_file = "${path.module}/../src/transformation.py"
  output_path = "${path.module}/../transformation_lambda.zip"

  depends_on = [null_resource.extraction]
}
data "archive_file" "loader_lambda" {
  /*
    Creates an archive file containing the Lambda function code and dependencies.

    Args:
        type (str): The type of archive file to create (e.g., "zip").
        source_file (str): The path to the main source file or directory to include in the archive.
        output_path (str): The path where the archive file will be generated.

    Returns:
        None
    */
  type        = "zip"
  source_file = "${path.module}/../src/loader.py"
  output_path = "${path.module}/../loader_lambda.zip"

  depends_on = [null_resource.extraction]
}

resource "null_resource" "extraction" {
  /*
    Creates a null resource that triggers the creation of an archive file containing the Lambda function code and dependencies.

    Args:
        triggers (dict): A dictionary specifying the trigger conditions for the null resource.

    Returns:
        None
    */
  triggers = {
    main = sha256(file("${path.module}/../src/extractor.py"))
  }
}
resource "null_resource" "transformation" {
  /*
    Creates a null resource that triggers the creation of an archive file containing the Lambda function code and dependencies.

    Args:
        triggers (dict): A dictionary specifying the trigger conditions for the null resource.

    Returns:
        None.
    */
  triggers = {
    main = sha256(file("${path.module}/../src/transformation.py"))
  }
}
resource "null_resource" "loader" {
  /*
    Creates a null resource that triggers the creation of an archive file containing the Lambda function code and dependencies.

    Args:
        triggers (dict): A dictionary specifying the trigger conditions for the null resource.

    Returns:
        None
    */
  triggers = {
    main = sha256(file("${path.module}/../src/loader.py"))
  }
}

data "aws_s3_bucket" "utility_bucket" {
  bucket = "${var.utility_bucket}"
}
