locals {

  cloud_sniper_tags = {
    Owner      = "Cloud Sniper"
    Department = "engineering"
    Purpose    = "Incident and Response Automation Bot Stack"
    TagVersion = "1.0"
  }

  region = "" # => Your region 

  main_account_id = "" # => Your account 

  dynamodb_name = "cloud-sniper-automated-actions"

  slack_automation_bot_secret = aws_secretsmanager_secret.slack_automation_bot_secret.name

}
