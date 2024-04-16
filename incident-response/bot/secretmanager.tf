resource "aws_secretsmanager_secret" "slack_automation_bot_secret" {
  name = "security-slack-automation-bot"
  tags = local.cloud_sniper_tags
}