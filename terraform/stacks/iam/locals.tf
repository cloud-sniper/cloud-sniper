locals {
  cloud_sniper_role_hub_iam_automation   = "cs-role-iam-automation"
  cloud_sniper_role_spoke_iam_automation = "cs-role-spoke-iam-automation"
  error_alarm_description                = "There was a potential Cloud Sniper IAM automation issue, check Lambda logs"

  cloud_sniper_tags = {
    Owner      = "Cloud Sniper"
    Department = "engineering"
    Purpose    = "Incident and Response Automation"
    TagVersion = "1.0"
  }

  # Customize
  hub_account_id   = "your account id"
  webhook_slack    = "your slack webhook"
  hub_account_name = "your account canonical name/alias"
}
