resource "aws_iam_policy" "cloudsniper_policy" {
  name   = "cloudsniper-policy"
  path   = "/"
  policy = "${data.aws_iam_policy_document.cloudsniper_policy_document.json}"
}

resource "aws_iam_policy" "cloudsniper_policy_tagging" {
  name   = "cloudsniper-policy-tagging"
  path   = "/"
  policy = "${data.aws_iam_policy_document.cloudsniper_policy_document_tagging.json}"
}

resource "aws_iam_policy" "cloudsniper_policy_tagging_incident_and_response" {
  name   = "cloudsniper-policy-tagging-incident-and-response"
  path   = "/"
  policy = "${data.aws_iam_policy_document.cloudsniper_policy_document_tagging_incident_and_response.json}"
}

resource "aws_iam_group" "cloudsniper_group_tagging_incident_and_response" {
  name = "cloudsniper-group-tagging-incident-and-response"
  path = "/"
}

resource "aws_iam_group_policy_attachment" "cloudsniper_group_policy_attachment_tagging" {
  group      = "${aws_iam_group.cloudsniper_group_tagging_incident_and_response.name}"
  policy_arn = "${aws_iam_policy.cloudsniper_policy_tagging_incident_and_response.arn}"
}

resource "aws_iam_role" "cloudsniper_role" {
  name               = "cloudsniper-role"
  path               = "/"
  assume_role_policy = "${data.aws_iam_policy_document.cloudsniper_policy_document_assume.json}"
}

resource "aws_iam_role" "cloudsniper_role_tagging" {
  name = "cloudsniper-role-tagging"
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

resource "aws_iam_role_policy_attachment" "cloudsniper_role_policy_attachment_lambda" {
  role       = "${aws_iam_role.cloudsniper_role.name}"
  policy_arn = "${aws_iam_policy.cloudsniper_policy.arn}"
}

resource "aws_iam_role_policy_attachment" "cloudsniper_role_policy_attachment_tagging" {
  role       = "${aws_iam_role.cloudsniper_role_tagging.name}"
  policy_arn = "${aws_iam_policy.cloudsniper_policy_tagging.arn}"
}

resource "aws_iam_role" "cloudsniper_role_firehose_waf" {
  name               = "cloudsniper-role-firehose-waf"
  assume_role_policy = "${data.aws_iam_policy_document.cloudsniper_policy_firehose.json}"
}

resource "aws_iam_role_policy" "cloudsniper_role_policy_kinesis_waf" {
  name = "cloudsniper-role-policy-kinesis-waf"
  role = "${aws_iam_role.cloudsniper_role_firehose_waf.id}"

  policy = "${data.aws_iam_policy_document.cloudsniper_policy_document_kinesis_waf.json}"
}
