resource "aws_cloudwatch_event_rule" "cloud_sniper_event_rule_schedule_security_ir_iam" {
  for_each            = { "infra" = local.hub_account_id } == { "infra" = data.aws_caller_identity.current.account_id } ? { hub : true } : {}
  name                = "cloud-sniper-event-rule-schedule-security-ir-iam"
  description         = "cloud-sniper-event-rule-schedule-security-ir-iam"
  schedule_expression = "cron(0 0 1,15 * ? *)"

  tags = local.cloud_sniper_tags
}

resource "aws_cloudwatch_event_target" "cloud_sniper_event_rule_schedule_security_ir_iam" {
  for_each = { "infra" = local.hub_account_id } == { "infra" = data.aws_caller_identity.current.account_id } ? { hub : true } : {}
  rule     = aws_cloudwatch_event_rule.cloud_sniper_event_rule_schedule_security_ir_iam["hub"].name
  arn      = aws_lambda_function.cloud_sniper_lambda_iam_automation["hub"].arn
}

resource "aws_cloudwatch_metric_alarm" "cloud_sniper_metric_alarm_security_ir" {
  for_each            = { "infra" = local.hub_account_id } == { "infra" = data.aws_caller_identity.current.account_id } ? { hub : true } : {}
  alarm_name          = "${aws_lambda_function.cloud_sniper_lambda_iam_automation["hub"].function_name}-errors"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  period              = "300"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  statistic           = "Sum"
  threshold           = "1"
  alarm_actions       = [aws_sns_topic.cloud_sniper_sns_topic_iam_automation_alert["hub"].arn]
  alarm_description   = local.error_alarm_description
  datapoints_to_alarm = "1"

  dimensions = {
    FunctionName = aws_lambda_function.cloud_sniper_lambda_iam_automation["hub"].function_name
  }

  tags = local.cloud_sniper_tags
}
