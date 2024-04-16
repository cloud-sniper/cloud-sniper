resource "aws_lambda_function" "open_security_groups_automation" {
  function_name    = "cloud-sniper-lambda-automation-open-security-groups"
  description      = "Cloud Sniper automation for security groups"
  handler          = "security_open_sg.lambda_handler"
  memory_size      = "1024"
  timeout          = "300"
  runtime          = "python3.6"
  filename         = data.archive_file.open_security_groups_automation.output_path
  source_code_hash = data.archive_file.open_security_groups_automation.output_base64sha256
  role             = aws_iam_role.assume_role_open_security_group_automation.arn

  tags = local.cloud_sniper_tags

  environment {
    variables = {
      DYNAMODB_NAME   = local.dynamodb_name,
      LAMBDA_BOT_NAME = local.bot_lambda_name
    }
  }
}

resource "aws_lambda_permission" "security_groups_automation_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudwatchRule"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.open_security_groups_automation.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.security_open_sg_automation_event.arn
}