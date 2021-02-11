resource "aws_iam_role" "dashboard_cloud_sniper_role" {
  name               = "dashboard-cloud-sniper-role"
  assume_role_policy = data.aws_iam_policy_document.dashboard_assume_policy_document.json
  tags               = local.cloud_sniper_tags
}

resource "aws_iam_role_policy" "cloudsniper_policy_dashboard" {
  name   = "cloudsniper-policy-dashboard"
  role   = aws_iam_role.dashboard_cloud_sniper_role.id
  policy = data.aws_iam_policy_document.dashboard_s3_access_policy_document.json
}


resource "aws_iam_instance_profile" "dashboard_instance_profile" {
  name = "cloudsniper_dashboard_profile"
  role = aws_iam_role.dashboard_cloud_sniper_role.name
}
