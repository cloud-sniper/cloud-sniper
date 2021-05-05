resource "aws_cloudwatch_event_rule" "cloud_sniper_event_rule_schedule_security_lusat" {
  name                = "cloud-sniper-event-rule-schedule-security-lusat"
  description         = "cloud-sniper-event-rule-schedule-security-lusat"
  schedule_expression = "rate(12 hours)"

  tags = local.cloud_sniper_tags
}


resource "aws_cloudwatch_event_target" "cloud_sniper_event_rule_schedule_security_lusat" {

  rule = aws_cloudwatch_event_rule.cloud_sniper_event_rule_schedule_security_lusat.name
  arn  = aws_lambda_function.cloud_sniper_lambda_lusat.arn

  input = <<INPUT
{
  "account_id": "${data.aws_caller_identity.current.account_id}",
  "role_assume": "${aws_iam_role.cloud_sniper_assume_role_lusat.name}",
  "inv": "all"
}
INPUT
}