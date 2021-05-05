
resource "aws_iam_role" "assume_role_open_security_group_automation" {
  name               = "open-security-group-automation"
  assume_role_policy = data.aws_iam_policy_document.assume_open_security_group_automation.json
}

resource "aws_iam_policy" "policy_open_security_group_automation" {
  name   = "policy-open-security-group-automation"
  policy = data.aws_iam_policy_document.open_security_group_automation.json
}

resource "aws_iam_role_policy_attachment" "attachment_open_security_group_automation" {
  role       = aws_iam_role.assume_role_open_security_group_automation.name
  policy_arn = aws_iam_policy.policy_open_security_group_automation.arn
}