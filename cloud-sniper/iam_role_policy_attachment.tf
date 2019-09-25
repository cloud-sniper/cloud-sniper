resource "aws_iam_role_policy_attachment" "iam_role_policy_attachment_lambda_cloud_sniper" {
  role       = "${aws_iam_role.role_cloud_sniper.name}"
  policy_arn = "${aws_iam_policy.iam_policy_cloud_sniper.arn}"
}

resource "aws_iam_role_policy_attachment" "iam_role_policy_attachment_cloud_sniper_tagging" {
  role       = "${aws_iam_role.role_cloud_sniper_tagging.name}"
  policy_arn = "${aws_iam_policy.iam_policy_cloud_sniper_tagging_sniffer.arn}"
}
