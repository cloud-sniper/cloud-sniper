locals {
  cloud_sniper_assume_role_threat_intelligence_automation = "cloud-sniper-assume-role-threat-intelligence-automation"
  cloud_sniper_role_spoke_threat_intelligence_automation  = "cloud-sniper-role-spoke-threat-intelligence-automation"
  cloud_sniper_sns_alarm_description                      = "There was a potential Cloud Sniper threat intelligence automation issue, check Lambda logs"

  cloud_sniper_tags = {
    Owner      = "Cloud Sniper"
    Department = "engineering"
    Purpose    = "Incident and Response Automation"
    TagVersion = "1.0"
  }

  # Customize
  hub_account_id = "[your-hub-id]"
  webhook_slack  = "https://hooks.slack.com/services/[your-id]"
}
