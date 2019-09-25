resource "aws_kinesis_firehose_delivery_stream" "aws_waf_logs_cloudsniper" {
  name        = "aws-waf-logs-cloudsniper"
  destination = "s3"

  s3_configuration {
    role_arn   = "${aws_iam_role.iam_role_firehose_waf.arn}"
    bucket_arn = "${aws_s3_bucket.s3_bucket_cloud_sniper_data_store.arn}"
  }
}
