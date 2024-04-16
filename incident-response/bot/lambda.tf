resource "aws_lambda_function" "slack_automation_bot" {
  function_name    = "cloud-sniper-slack-automation-bot"
  description      = "Cloud Sniper - Automation Bot"
  handler          = "send_to_slack.lambda_handler"
  memory_size      = "1024"
  timeout          = "300"
  runtime          = "python3.6"
  filename         = data.archive_file.slack_automation_bot.output_path
  source_code_hash = data.archive_file.slack_automation_bot.output_base64sha256
  role             = aws_iam_role.assume_role_slack_automation_bot.arn

  tags = local.cloud_sniper_tags

  environment {
    variables = {
      SLACK_AUTOMATION_BOT = local.slack_automation_bot_secret
    }
  }
}

resource "aws_lambda_function" "slack_automation_bot_button" {
  function_name    = "cloud-sniper-slack-automation-bot-button"
  description      = "Cloud Sniper - Automation Bot - Button Handler"
  handler          = "button_actions.lambda_handler"
  memory_size      = "1024"
  timeout          = "300"
  runtime          = "python3.6"
  filename         = data.archive_file.slack_automation_bot.output_path
  source_code_hash = data.archive_file.slack_automation_bot.output_base64sha256
  role             = aws_iam_role.assume_role_slack_automation_bot_button.arn

  tags = local.cloud_sniper_tags

  environment {
    variables = {
      SLACK_AUTOMATION_BOT = local.slack_automation_bot_secret,
      DYNAMODB_NAME        = local.dynamodb_name
    }
  }
}

resource "aws_lambda_permission" "slack_automation_bot_button" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.slack_automation_bot_button.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.slack_automation_bot_button.execution_arn}/*/*/slack/automation"
}
