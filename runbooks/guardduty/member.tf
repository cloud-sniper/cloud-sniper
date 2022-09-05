resource "aws_guardduty_member" "guardduty_members_security" {
  count              = length(local.account_ids_except_current)
  detector_id        = aws_guardduty_detector.cloud_sniper_guardduty_main_detector_region.id
  invite             = "true"
  invitation_message = local.invitation_message_guardduty
  account_id         = element(local.account_ids_except_current, count.index)

  #add your email format
  email = format("format@domain.com", element(local.account_names_except_current, count.index))
}
