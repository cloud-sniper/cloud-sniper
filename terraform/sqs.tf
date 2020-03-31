resource "aws_sqs_queue" "cloudsniper_sqs_queue" {
  name = "cloudsniper_sqs_queue"
}

resource "aws_sqs_queue_policy" "cloudsniper_sqs_queue_policy" {
  queue_url = "${aws_sqs_queue.cloudsniper_sqs_queue.id}"

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
      "Resource": "${aws_sqs_queue.cloudsniper_sqs_queue.arn}",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${aws_cloudwatch_event_rule.cloudsniper_cloudwatch_event_rule.arn}"
        }
      }
    }
  ]
}
POLICY
}
