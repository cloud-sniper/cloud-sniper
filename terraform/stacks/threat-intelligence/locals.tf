locals {
  cloud_sniper_assume_role_threat_intelligence_automation = "cs-assume-role-threat-intelligence-automation"
  cloud_sniper_role_spoke_threat_intelligence_automation  = "cs-role-spoke-threat-intelligence-automation"
  cloud_sniper_sns_alarm_description                      = "There was a potential Cloud Sniper threat intelligence automation issue, check Lambda logs"

  cloud_sniper_tags = {
    Owner      = "Cloud Sniper"
    Department = "engineering"
    Purpose    = "Incident and Response Automation"
    TagVersion = "1.0"
  }

  # Customize
  hub_account_id = "[customize]"
  webhook_slack  = "[customize]"
}
