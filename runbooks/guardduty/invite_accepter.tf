resource "aws_guardduty_invite_accepter" "cloud_sniper_invite_accepter" {
  count             = data.aws_caller_identity.current.account_id == local.hub_account_id ? 0 : 1
  detector_id       = aws_guardduty_detector.cloud_sniper_guardduty_detector_region.id
  master_account_id = local.hub_account_id
}
