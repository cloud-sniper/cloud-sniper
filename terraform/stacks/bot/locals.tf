locals {

  cloud_sniper_tags = {
    Owner      = "Cloud Sniper"
    Department = "engineering"
    Purpose    = "Incident and Response Automation Bot Stack"
    TagVersion = "1.0"
  }

  region = "us-west-2"

  main_account_id = "551784954523"

  dynamodb_name = "cloud-sniper-automated-actions"

  slack_automation_bot_secret = aws_secretsmanager_secret.slack_automation_bot_secret.name

}
