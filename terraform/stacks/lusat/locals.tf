locals {
  cloud_sniper_role_hub_lusat   = "cs-role-lusat"
  cloud_sniper_role_spoke_lusat = "cs-role-spoke-lusat"
  error_alarm_description       = "There was a potential Cloud Sniper - Lusat issue, check Lambda logs"
  region                        = "us-west-2"
  cloud_sniper_tags = {
    Owner      = "Cloud Sniper"
    Department = "engineering"
    Purpose    = "Incident and Response Automation"
    Function   = "cloud-lusat"
    TagVersion = "1.0"
  }

  # Customize
  hub_account_id   = "your account id"
  webhook_slack    = "your slack webhook"
  hub_account_name = "your account canonical name/alias"
}
