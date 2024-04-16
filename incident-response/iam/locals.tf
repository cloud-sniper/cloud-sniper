locals {
  is_hub_account   = local.hub_account_id == data.aws_caller_identity.current.account_id ? { hub : true } : {}
  is_spoke_account = local.hub_account_id == data.aws_caller_identity.current.account_id ? {} : { spoke : true }

  # IAM role names
  cloud_sniper_role_hub_iam_automation   = "cs-role-iam-automation"
  cloud_sniper_role_spoke_iam_automation = "cs-role-spoke-iam-automation"

  # Alarm description
  error_alarm_description = "There was a potential Cloud Sniper IAM automation issue, check Lambda logs"

  # Tags for Cloud Sniper resources
  cloud_sniper_tags = {
    Owner      = "Cloud Sniper"
    Department = "engineering"
    Purpose    = "Incident and Response Automation"
    TagVersion = "1.0"
  }

  # Customizable variables
  hub_account_id   = "[account-id]"
  webhook_slack    = "[https://hooks.slack.com/services/xxxx]"
  hub_account_name = "[account-name]"

  # Path for IAM Indicators of Compromise (IOCs) outputs
  cloud_sniper_iam_path = "/iam"

  # S3 bucket for data storage
  cloud_sniper_data_store = "[s3-data-store]"
}
