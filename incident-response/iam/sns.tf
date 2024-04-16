resource "aws_sns_topic" "cloud_sniper_sns_topic_iam_automation_alert" {
  for_each = local.is_hub_account ? { hub : true } : {}
  name     = "cloud-sniper-sns-topic-iam-automation-alert"
}
