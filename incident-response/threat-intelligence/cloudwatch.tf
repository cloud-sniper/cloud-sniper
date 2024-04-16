resource "aws_cloudwatch_event_rule" "cloud_sniper_cloudwatch_event_rule_threat_intelligence_automation" {
  for_each    = local.is_hub_account ? { hub : true } : {}
  name        = "cloud-sniper-event-rule-threat-intelligence"
  description = "cloud-sniper-event-rule-threat-intelligence"

  event_pattern = <<PATTERN
{
  "source": [
    "aws.guardduty"
  ],
  "detail-type": [
    "GuardDuty Finding"
  ]
}
PATTERN

  tags = local.cloud_sniper_tags
}

resource "aws_cloudwatch_event_rule" "cloud_sniper_cloudwatch_event_rule_schedule_threat_intelligence_automation" {
  for_each            = local.is_hub_account ? { hub : true } : {}
  name                = "cloud-sniper-event-rule-schedule-threat-intelligence"
  description         = "cloud-sniper-event-rule-schedule-threat-intelligence"
  schedule_expression = "rate(5 minutes)"

  tags = local.cloud_sniper_tags
}

resource "aws_cloudwatch_event_target" "cloud_sniper_cloudwatch_event_target_threat_intelligence_automation" {
  for_each = local.is_hub_account ? { hub : true } : {}
  rule     = aws_cloudwatch_event_rule.cloud_sniper_cloudwatch_event_rule_threat_intelligence_automation["hub"].name
  arn      = aws_sqs_queue.cloud_sniper_sqs_queue_threat_intelligence_automation["hub"].arn
}

resource "aws_cloudwatch_event_target" "cloud_sniper_cloudwatch_event_rule_schedule_threat_intelligence_automation" {
  for_each = local.is_hub_account ? { hub : true } : {}
  rule     = aws_cloudwatch_event_rule.cloud_sniper_cloudwatch_event_rule_schedule_threat_intelligence_automation["hub"].name
  arn      = aws_lambda_function.cloud_sniper_lambda_threat_intelligence_automation["hub"].arn
}

resource "aws_cloudwatch_metric_alarm" "cloud_sniper_cloudwatch_metric_alarm_threat_intelligence_automation" {
  for_each = local.is_hub_account ? { hub : true } : {}

  alarm_name          = "${aws_lambda_function.cloud_sniper_lambda_threat_intelligence_automation["hub"].function_name}-errors"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  period              = "300"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  statistic           = "Sum"
  threshold           = "1"
  alarm_actions       = [aws_sns_topic.cloud_sniper_sns_topic_threat_intelligence_alert["hub"].arn]
  alarm_description   = local.cloud_sniper_sns_alarm_description
  datapoints_to_alarm = "1"

  dimensions = {
    FunctionName = aws_lambda_function.cloud_sniper_lambda_threat_intelligence_automation["hub"].function_name
  }

  tags = local.cloud_sniper_tags
}
