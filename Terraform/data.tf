data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "archive_file" "lambda" {
    type = "zip"
    source_file = "${path.module}/../src/extractor.py"
    output_path = "${path.module}/../extraction_lambda.zip"

    depends_on = [null_resource.sauce]
}

resource "null_resource" "sauce" {
  triggers = {
    main = sha256(file("${path.module}/../src/extractor.py"))
  }
}