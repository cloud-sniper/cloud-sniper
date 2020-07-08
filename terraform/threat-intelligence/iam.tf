#all spoke accounts
resource "aws_iam_role" "cloud_sniper_role_spoke_threat_intelligence_automation" {
  for_each           = { "hub" = local.hub_account_id } == { "hub" = data.aws_caller_identity.current.account_id } ? {} : { spoke : true }
  name               = "cloud-sniper-role-spoke-threat-intelligence-automation"
  assume_role_policy = data.aws_iam_policy_document.cloud_sniper_policy_document_assume_spoke_threat_intelligence_automation.json
  tags               = local.cloud_sniper_tags
}

resource "aws_iam_policy" "cloud_sniper_policy_spoke_threat_intelligence_automation" {
  for_each = { "hub" = local.hub_account_id } == { "hub" = data.aws_caller_identity.current.account_id } ? {} : { spoke : true }
  name     = "cloud-sniper-policy-spoke-threat-intelligence-automation"
  policy   = data.aws_iam_policy_document.cloud_sniper_policy_document_spoke_threat_intelligence_automation.json
}

resource "aws_iam_role_policy_attachment" "cloud_sniper_role_policy_attachment_spoke_threat_intelligence_automation" {
  for_each   = { "hub" = local.hub_account_id } == { "hub" = data.aws_caller_identity.current.account_id } ? {} : { spoke : true }
  role       = aws_iam_role.cloud_sniper_role_spoke_threat_intelligence_automation[each.key].name
  policy_arn = aws_iam_policy.cloud_sniper_policy_spoke_threat_intelligence_automation[each.key].arn
}

#hub account
resource "aws_iam_role" "cloud_sniper_role_threat_intelligence_automation" {
  for_each           = { "hub" = local.hub_account_id } == { "hub" = data.aws_caller_identity.current.account_id } ? { hub : true } : {}
  name               = "cs-assume-role-threat-intelligence-automation-${data.aws_region.current.name}"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.cloud_sniper_policy_document_assume_threat_intelligence_automation.json
  tags               = local.cloud_sniper_tags
}

resource "aws_iam_policy" "cloud_sniper_policy_threat_intelligence_automation" {
  for_each = { "hub" = local.hub_account_id } == { "hub" = data.aws_caller_identity.current.account_id } ? { hub : true } : {}
  name     = "cs-policy-threat-intelligence-automation-${data.aws_region.current.name}"
  policy   = data.aws_iam_policy_document.cloud_sniper_policy_document_threat_intelligence_automation["hub"].json
}

resource "aws_iam_role_policy_attachment" "cloud_sniper_role_policy_attachment_threat_intelligence_automation" {
  for_each   = { "hub" = local.hub_account_id } == { "hub" = data.aws_caller_identity.current.account_id } ? { hub : true } : {}
  role       = aws_iam_role.cloud_sniper_role_threat_intelligence_automation["hub"].name
  policy_arn = aws_iam_policy.cloud_sniper_policy_threat_intelligence_automation["hub"].arn
}

## Analytics
#hub account
resource "aws_iam_role" "cloud_sniper_role_beaconing_detection" {
  for_each           = { "hub" = local.hub_account_id } == { "hub" = data.aws_caller_identity.current.account_id } ? { hub : true } : {}
  name               = "cs-assume-role-beaconing-detection-${data.aws_region.current.name}"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.cloud_sniper_policy_document_assume_beaconing_detection.json
}

resource "aws_iam_policy" "cloud_sniper_policy_beaconing_detection" {
  for_each = { "hub" = local.hub_account_id } == { "hub" = data.aws_caller_identity.current.account_id } ? { hub : true } : {}
  name     = "cs-policy-beaconing-detection-${data.aws_region.current.name}"
  path     = "/"
  policy   = data.aws_iam_policy_document.cloud_sniper_policy_document_beaconing_detection.json
}

resource "aws_iam_role_policy_attachment" "cloud_sniper_role_policy_attachment_beaconing_detection" {
  for_each   = { "hub" = local.hub_account_id } == { "hub" = data.aws_caller_identity.current.account_id } ? { hub : true } : {}
  role       = aws_iam_role.cloud_sniper_role_beaconing_detection["hub"].name
  policy_arn = aws_iam_policy.cloud_sniper_policy_beaconing_detection["hub"].arn
}
