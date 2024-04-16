resource "aws_cloudwatch_event_rule" "security_open_sg_automation_event" {
  name        = "cloud-sniper-open-sg-automated-action"
  description = "capture sg creation and run lambda automation"
  tags        = local.cloud_sniper_tags

  event_pattern = <<PATTERN
  {
    "source": [
      "aws.ec2"
    ],
    "detail-type": [
      "AWS API Call via CloudTrail"
    ],
    "detail": {
      "eventSource": [
        "ec2.amazonaws.com"
      ],
      "eventName": [
        "AuthorizeSecurityGroupIngress"
      ]
    }
  }
PATTERN
}


resource "aws_cloudwatch_event_target" "security_open_sg_automation_target" {
  rule      = aws_cloudwatch_event_rule.security_open_sg_automation_event.name
  target_id = "SendToLAMBDA"
  arn       = aws_lambda_function.open_security_groups_automation.arn
}
