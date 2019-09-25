resource "aws_sqs_queue_policy" "sqs_queue_policy_cloud_sniper" {
  queue_url = "${aws_sqs_queue.sqs_queue_cloud_sniper.id}"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqspolicycloudsniper",
  "Statement": [
    {
      "Sid": "sqspolicycloudsniper",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.sqs_queue_cloud_sniper.arn}",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${aws_cloudwatch_event_rule.aws_cloudwatch_event_rule_cloud_sniper.arn}"
        }
      }
    }
  ]
}
POLICY
}
