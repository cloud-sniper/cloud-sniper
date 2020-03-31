resource "aws_kinesis_firehose_delivery_stream" "cloudsniper_aws_waf_logs" {
  name        = "cloudsniper-aws-waf-logs"
  destination = "s3"

  s3_configuration {
    role_arn   = "${aws_iam_role.cloudsniper_role_firehose_waf.arn}"
    bucket_arn = "${aws_s3_bucket.cloudsniper_s3_bucket_data_store.arn}"
  }
}
