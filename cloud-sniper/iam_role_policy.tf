resource "aws_iam_role_policy" "iam_role_policy_kinesis_waf" {
  name = "iam_role_policy_kinesis_waf"
  role = "${aws_iam_role.iam_role_firehose_waf.id}"

  policy = "${data.aws_iam_policy_document.iam_policy_document_kinesis_waf.json}"
}
