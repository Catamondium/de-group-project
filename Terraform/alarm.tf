resource "aws_cloudwatch_log_metric_filter" "create_cloudwatch_log_group" {
    name = "ReadError"
    pattern = "ERROR"
    log_group_name = aws_cloudwatch_log_group.create_cloudwatch_log_group.name

    metric_transformation {
      name = "ErrorMetric"
      namespace = "ExtractionLambdaError"
      value = 1
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_errors" {
  alarm_name          = "ErrorAlert"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  metric_name         = "ErrorMetric"
  namespace           = "ExtractionLambdaError"
  evaluation_periods  = 1
  period              = 60
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "This triggers when ConnectionErrorAlert is triggered in a minute."
  alarm_actions = ["arn:aws:sns:eu-west-2:730335327822:ConnectionErrorTest"]
  actions_enabled = "true"
} 

