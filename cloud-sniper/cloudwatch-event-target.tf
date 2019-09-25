resource "aws_cloudwatch_event_target" "aws_cloudwatch_event_target_cloud_sniper" {
  rule = "${aws_cloudwatch_event_rule.aws_cloudwatch_event_rule_cloud_sniper.name}"
  arn  = "${aws_sqs_queue.sqs_queue_cloud_sniper.arn}"
}

resource "aws_cloudwatch_event_target" "aws_cloudwatch_event_rule_schedule_cloud_sniper" {
  rule = "${aws_cloudwatch_event_rule.aws_cloudwatch_event_rule_schedule_cloud_sniper.name}"
  arn  = "${aws_lambda_function.lambda_function_cloud_sniper.arn}"
}

resource "aws_cloudwatch_event_target" "cloudwatch_event_target_cloud_sniper_tagging" {
  rule = "${aws_cloudwatch_event_rule.cloudwatch_event_rule_cloud_sniper_tagging.name}"
  arn  = "${aws_lambda_function.lambda_function_cloud_sniper_tagging_ir.arn}"
}
