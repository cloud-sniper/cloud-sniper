# Creates GuardDuty members for all accounts except the current account
resource "aws_guardduty_member" "guardduty_members_security" {
  count              = length(local.account_ids_except_current)
  detector_id        = aws_guardduty_detector.cloud_sniper_guardduty_main_detector_region.id
  invite             = "true"
  invitation_message = local.invitation_message_guardduty
  account_id         = element(local.account_ids_except_current, count.index)

  # Formats the email address for each member using the account name and the email domain
  email = format("%s@%s", element(local.account_names_except_current, count.index), var.email_domain)
}
