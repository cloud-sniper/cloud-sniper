resource "aws_lambda_function" "cloud_sniper_lambda_iam_automation" {
  for_each         = { "infra" = local.hub_account_id } == { "infra" = data.aws_caller_identity.current.account_id } ? { hub : true } : {}
  function_name    = "cloud-sniper-lambda-iam-automation"
  description      = "Cloud Sniper Incident and Response IAM automation"
  handler          = "cloud_sniper_iam.cloud_sniper_iam"
  memory_size      = "1024"
  timeout          = "300"
  runtime          = "python3.6"
  filename         = data.archive_file.cloud_sniper_lambda_iam_automation.output_path
  source_code_hash = data.archive_file.cloud_sniper_lambda_iam_automation.output_base64sha256
  role             = aws_iam_role.cloud_sniper_assume_role_iam_automation["hub"].arn

  environment {
    variables = {
      WEBHOOK_URL_CLOUD_SNIPER      = local.webhook_slack
      HUB_ACCOUNT_CLOUD_SNIPER      = local.hub_account_id
      ROLE_SPOKE_CLOUD_SNIPER       = format("%s-%s", local.cloud_sniper_role_spoke_iam_automation, data.aws_region.current.name)
      HUB_ACCOUNT_NAME_CLOUD_SNIPER = local.hub_account_name
      BUCKET_NAME                   = local.cloud_sniper_data_store
      IAM_PATH                      = local.cloud_sniper_iam_path
    }
  }

  tags = local.cloud_sniper_tags
}
