#all spoke accounts
resource "aws_iam_role" "cloud_sniper_role_spoke_iam_automation" {
  for_each           = local.hub_account_id == data.aws_caller_identity.current.account_id ? {} : { spoke : true }
  name               = "cs-role-spoke-iam-automation-${data.aws_region.current.name}"
  assume_role_policy = data.aws_iam_policy_document.cloud_sniper_policy_document_spoke_assume_iam_automation.json
}

resource "aws_iam_policy" "cloud_sniper_policy_spoke_iam_automation" {
  for_each = local.hub_account_id == data.aws_caller_identity.current.account_id ? {} : { spoke : true }
  name     = "policy-spoke-poc-config-security-ir-automation-${data.aws_region.current.name}"
  policy   = data.aws_iam_policy_document.cloud_sniper_policy_document_spoke_iam_automation.json
}

resource "aws_iam_role_policy_attachment" "cloud_sniper_iam_role_policy_attachment_spoke_iam_automation" {
  for_each   = local.hub_account_id == data.aws_caller_identity.current.account_id ? {} : { spoke : true }
  role       = aws_iam_role.cloud_sniper_role_spoke_iam_automation["spoke"].name
  policy_arn = aws_iam_policy.cloud_sniper_policy_spoke_iam_automation["spoke"].arn
}

# main account
resource "aws_iam_role" "cloud_sniper_assume_role_iam_automation" {
  for_each           = local.hub_account_id == data.aws_caller_identity.current.account_id ? { hub : true } : {}
  name               = "cs-role-iam-automation-${data.aws_region.current.name}"
  assume_role_policy = data.aws_iam_policy_document.cloud_sniper_policy_document_assume_iam_automation.json
}

resource "aws_iam_policy" "cloud_sniper_policy_iam_automation" {
  for_each = local.hub_account_id == data.aws_caller_identity.current.account_id ? { hub : true } : {}
  name     = "policy-security-ir-automation-iam-${data.aws_region.current.name}"
  policy   = data.aws_iam_policy_document.cloud_sniper_policy_document_iam_automation.json
}

resource "aws_iam_role_policy_attachment" "cloud_sniper_iam_role_policy_attachment_iam_automation" {
  for_each   = local.hub_account_id == data.aws_caller_identity.current.account_id ? { hub : true } : {}
  role       = aws_iam_role.cloud_sniper_assume_role_iam_automation["hub"].name
  policy_arn = aws_iam_policy.cloud_sniper_policy_iam_automation["hub"].arn
}
