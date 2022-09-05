resource "aws_sns_topic" "cloud_sniper_sns_topic_iam_automation_alert" {
  for_each = local.hub_account_id == data.aws_caller_identity.current.account_id ? { hub : true } : {}
  name     = "cloud-sniper-sns-topic-iam-automation-alert"
}
