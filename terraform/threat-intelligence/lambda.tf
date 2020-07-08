resource "aws_lambda_function" "cloud_sniper_lambda_threat_intelligence_automation" {
  for_each         = { "hub" = local.hub_account_id } == { "hub" = data.aws_caller_identity.current.account_id } ? { hub : true } : {}
  function_name    = "cloud-sniper-lambda-threat-intelligence-automation"
  description      = "Cloud Sniper threat intelligence automation"
  handler          = "cloud_sniper_threat_intelligence.security_ir"
  memory_size      = 1024
  timeout          = 300
  runtime          = "python3.6"
  filename         = data.archive_file.cloud_sniper_archive_threat_intelligence_automation.output_path
  source_code_hash = data.archive_file.cloud_sniper_archive_threat_intelligence_automation.output_base64sha256
  role             = aws_iam_role.cloud_sniper_role_threat_intelligence_automation["hub"].arn

  environment {
    variables = {
      SQS_QUEUE_CLOUD_SNIPER      = aws_sqs_queue.cloud_sniper_sqs_queue_threat_intelligence_automation["hub"].id
      DYNAMO_TABLE_CLOUD_SNIPER   = aws_dynamodb_table.cloud_sniper_table["hub"].name
      WEBHOOK_URL_IR              = local.webhook_slack
      HUB_ACCOUNT_ID_CLOUD_SNIPER = local.hub_account_id
      ROLE_SPOKE_CLOUD_SNIPER     = local.cloud_sniper_role_spoke_threat_intelligence_automation
      BUCKET_NAME                 = aws_s3_bucket.cloud_sniper_s3_bucket_data_store["hub"].id
      IOCS_PATH                   = var.cloud_sniper_iocs_path
    }
  }

  tags = local.cloud_sniper_tags
}

resource "aws_lambda_function" "cloud_sniper_lambda_beaconing_detection" {
  for_each      = { "hub" = local.hub_account_id } == { "hub" = data.aws_caller_identity.current.account_id } ? { hub : true } : {}
  function_name = "cloud-sniper-lambda-beaconing-detection"
  description   = "Cloud Sniper beaconing detection"
  handler       = "cloud_sniper_beaconing_detection.cloud_sniper_beaconing_detection"
  s3_bucket     = aws_s3_bucket.cloud_sniper_s3_bucket_data_store["hub"].id
  s3_key        = "cloud_sniper_beaconing_detection.zip"
  memory_size   = 1024
  timeout       = 300
  role          = aws_iam_role.cloud_sniper_role_beaconing_detection["hub"].arn
  runtime       = "python3.6"

  environment {
    variables = {
      BUCKET_NAME        = aws_s3_bucket.cloud_sniper_s3_bucket_data_store["hub"].id
      VPC_FLOW_LOGS_PATH = var.cloud_sniper_beaconing_flows_path
      FINDINGS_PATH      = var.cloud_sniper_beaconing_findings_path
    }
  }
}
