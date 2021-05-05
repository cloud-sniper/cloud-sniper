# main account
resource "aws_iam_role" "cloud_sniper_assume_role_lusat" {
  name               = "cs-role-lusat-${data.aws_region.current.name}"
  assume_role_policy = data.aws_iam_policy_document.cloud_sniper_policy_document_assume_lusat.json
}

resource "aws_iam_policy" "cloud_sniper_policy_lusat" {
  name   = "policy-security-lusat-${data.aws_region.current.name}"
  policy = data.aws_iam_policy_document.cloud_sniper_policy_document_lusat.json
}

resource "aws_iam_role_policy_attachment" "cloud_sniper_iam_role_policy_attachment_lusat" {
  role       = aws_iam_role.cloud_sniper_assume_role_lusat.name
  policy_arn = aws_iam_policy.cloud_sniper_policy_lusat.arn
}
