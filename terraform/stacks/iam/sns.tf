resource "aws_sns_topic" "cloud_sniper_sns_topic_iam_automation_alert" {
  for_each = { "infra" = local.hub_account_id } == { "infra" = data.aws_caller_identity.current.account_id } ? { hub : true } : {}
  name     = "cloud-sniper-sns-topic-iam-automation-alert"
}
