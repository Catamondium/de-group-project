resource "aws_iam_role" "extraction_lambda_role" {
  assume_role_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Effect" : "Allow",
          "Action" : [
            "sts:AssumeRole"
          ],
          "Principal" : {
            "Service" : [
              "lambda.amazonaws.com"
            ]
          }
        }
      ]
    }
  )
}

# policy and roles for the put s3 document
data "aws_iam_policy_document" "put_s3_document" {
  statement {
    actions = ["s3:PutObject"]
    resources = [
      "${aws_s3_bucket.rannoch-s3-ingestion-bucket.arn}"
    ]
  }
}

data "aws_iam_policy_document" "cw_document" {
  statement {
    actions = ["logs:CreateLogGroup"]

    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
    ]
  }

  statement {
    actions = ["logs:CreateLogStream", "logs:PutLogEvents"]

    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${aws_lambda_function.extraction_lambda.function_name}:*"
      # add the transform lambda role here 
    ]
  }
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.extraction_lambda.function_name}"
  principal     = "events.amazonaws.com"
  #source_account = "${data.aws_caller_identity.current.account_id}"
  source_arn    = "${aws_cloudwatch_event_rule.every_five_minutes.arn}"
  #qualifier     = aws_lambda_alias.test_alias.name
}

resource "aws_iam_policy" "s3_policy" {
  name_prefix = "s3-policy-${var.bucket_name}"
  policy      = data.aws_iam_policy_document.put_s3_document.json
}

resource "aws_iam_role_policy_attachment" "lambda_s3_policy_attachment" {
  role       = aws_iam_role.extraction_lambda_role.name
  policy_arn = aws_iam_policy.s3_policy.arn
}

resource "aws_iam_policy" "cloudwatch_policy" {
  name_prefix = "cw-policy-${var.ingestion_lambda_name}"
  policy      = data.aws_iam_policy_document.cw_document.json
}

resource "aws_iam_role_policy_attachment" "lambda_cw_policy_attachment" {
  role       = aws_iam_role.extraction_lambda_role.name
  policy_arn = aws_iam_policy.cloudwatch_policy.arn
}

