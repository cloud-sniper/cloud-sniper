resource "aws_iam_group_policy_attachment" "iam_group_policy_attachment_cloudsniper_tagging" {
  group      = "${aws_iam_group.iam_group_cloud_sniper_tagging_incident_and_response.name}"
  policy_arn = "${aws_iam_policy.iam_policy_cloud_sniper_tagging_incident_and_response.arn}"
}
