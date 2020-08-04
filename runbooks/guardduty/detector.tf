resource "aws_guardduty_detector" "cloud_sniper_guardduty_detector_region" {
  count                        = data.aws_caller_identity.current.account_id == local.hub_account_id ? 0 : 1
  enable                       = var.enable
  finding_publishing_frequency = "FIFTEEN_MINUTES"
}
resource "aws_guardduty_detector" "cloud_sniper_guardduty_main_detector_region" {
  count                        = data.aws_caller_identity.current.account_id == local.hub_account_id ? 1 : 0
  enable                       = var.enable
  finding_publishing_frequency = "FIFTEEN_MINUTES"
}
