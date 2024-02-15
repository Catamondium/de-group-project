resource "aws_cloudwatch_event_rule" "every_five_minutes" {
  name                = "every-five-minutes"
  description         = "Fires every five minutes"
  # will be much less frequent
  schedule_expression = "rate(1 minute)"
  #role_arn = "${aws_lambda_permission.allow_cloudwatch.arn}" 
}
resource "aws_cloudwatch_event_target" "every_five_minutes" {
  rule      = aws_cloudwatch_event_rule.every_five_minutes.name
  target_id = "extraction_lambda"
  arn       = "${aws_lambda_function.extraction_lambda.arn}"
}

resource "aws_cloudwatch_log_group" "create_cloudwatch_log_group" {
  name = "/aws/lambda/${aws_lambda_function.extraction_lambda.function_name}"
}