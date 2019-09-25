resource "aws_iam_role" "role_cloud_sniper" {
  name               = "role_cloud_sniper"
  path               = "/"
  assume_role_policy = "${data.aws_iam_policy_document.iam_policy_lambda.json}"
}

resource "aws_iam_role" "iam_role_firehose_waf" {
  name               = "iam_role_firehose_waf"
  assume_role_policy = "${data.aws_iam_policy_document.iam_policy_firehose.json}"
}

resource "aws_iam_role" "role_cloud_sniper_tagging" {
  name = "role_cloud_sniper_tagging"
  path = "/"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]

}
EOF
}
