resource "aws_cloudwatch_event_rule" "cloudsniper_cloudwatch_event_rule" {
  name = "cloudsniper-cloudwatch-event-rule"

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

resource "aws_cloudwatch_event_rule" "cloudsniper_cloudwatch_event_rule_scheduler" {
  name                = "cloudsniper-cloudwatch-event-rule-scheduler"
  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_rule" "cloudsniper_cloudwatch_event_rule_tagging" {
  name        = "cloudsniper-cloudwatch-event-rule-tagging"
  description = "Triggers anytime an EC2 instance, EBS volume, EBS Snapshot or AMI is created"

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

resource "aws_cloudwatch_event_target" "cloudsniper_cloudwatch_event_target" {
  rule = "${aws_cloudwatch_event_rule.cloudsniper_cloudwatch_event_rule.name}"
  arn  = "${aws_sqs_queue.cloudsniper_sqs_queue.arn}"
}

resource "aws_cloudwatch_event_target" "cloudsniper_cloudwatch_event_target_scheduler" {
  rule = "${aws_cloudwatch_event_rule.cloudsniper_cloudwatch_event_rule_scheduler.name}"
  arn  = "${aws_lambda_function.cloudsniper_lambda_function_ir.arn}"
}

resource "aws_cloudwatch_event_target" "cloudsniper_cloudwatch_event_target_tagging" {
  rule = "${aws_cloudwatch_event_rule.cloudsniper_cloudwatch_event_rule_tagging.name}"
  arn  = "${aws_lambda_function.cloudsniper_lambda_function_tagging_ir.arn}"
}
