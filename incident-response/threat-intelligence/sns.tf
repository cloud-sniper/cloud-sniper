resource "aws_sns_topic" "cloud_sniper_sns_topic_threat_intelligence_alert" {
  for_each = local.is_hub_account ? { hub : true } : {}
  name     = "cloud-sniper-sns-topic-threat-intelligence-alert"
}

resource "aws_sns_topic" "cloud_sniper_sns_topic_threat_intelligence" {
  for_each = local.is_hub_account ? { hub : true } : {}
  name     = "cloud-sniper-sns-topic-threat-intelligence"
}

resource "aws_sns_topic_subscription" "cloud_sniper_sns_subscription_threat_intelligence" {
  for_each  = local.is_hub_account ? { hub : true } : {}
  topic_arn = aws_sns_topic.cloud_sniper_sns_topic_threat_intelligence["hub"].arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.cloud_sniper_lambda_beaconing_detection["hub"].arn
}
