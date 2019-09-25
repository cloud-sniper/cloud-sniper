resource "aws_cloudwatch_event_rule" "aws_cloudwatch_event_rule_cloud_sniper" {
  name        = "aws_cloudwatch_event_rule_cloud_sniper"
  description = "aws_cloudwatch_event_rule_cloud_sniper"

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
}

resource "aws_cloudwatch_event_rule" "aws_cloudwatch_event_rule_schedule_cloud_sniper" {
  name                = "aws_cloudwatch_event_rule_schedule_cloud_sniper"
  description         = "aws_cloudwatch_event_rule_schedule_cloud_sniper"
  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_rule" "cloudwatch_event_rule_cloud_sniper_tagging" {
  name        = "cloudwatch_event_rule_cloud_sniper_tagging"
  description = "Trigger anytime an EC2 instance, EBS volume, EBS Snapshot or AMI is created"

  event_pattern = <<PATTERN
{
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "detail": {
    "eventSource": [
      "ec2.amazonaws.com"
    ],
    "eventName": [
      "CreateVolume",
      "RunInstances",
      "CreateImage",
      "CreateSnapshot"
    ]
  }
}
PATTERN
}
