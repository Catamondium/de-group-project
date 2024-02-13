# module "eventbridge" {
#   source = "terraform-aws-modules/eventbridge/aws"

#   bus_name = "5 minutes extraction loop" 

#   attach_lambda_policy = true
#   lambda_target_arns   = ["${aws_lambda_function.extraction_lambda.arn}"]

#   schedules = {
#     lambda-cron = {
#       description         = "Trigger for a Lambda"
#       schedule_expression = "rate(5 minutes)"
#       timezone            = "Europe/London"
#       arn                 = "${aws_lambda_function.extraction_lambda.arn}"
#     }
#   }
# }

resource "aws_cloudwatch_event_rule" "every_five_minutes" {
  name                = "every-five-minutes"
  description         = "Fires every five minutes"
  schedule_expression = "rate(5 minutes)"
}
resource "aws_cloudwatch_event_target" "every_five_minutes" {
  rule      = aws_cloudwatch_event_rule.every_five_minutes.name
  target_id = "extraction_lambda"
  arn       = "${aws_lambda_function.extraction_lambda.arn}"
}

resource "aws_cloudwatch_log_group" "create_cloudwatch_log_group" {
  name = "/aws/lambda/${aws_lambda_function.extraction_lambda.function_name}"
}