resource "aws_apigatewayv2_api" "slack_automation_bot_button" {
  name          = "slack-automation-bot"
  protocol_type = "HTTP"
  target        = aws_lambda_function.slack_automation_bot_button.arn

  tags = local.cloud_sniper_tags
}

resource "aws_apigatewayv2_integration" "slack_automation_bot_button" {
  api_id                 = aws_apigatewayv2_api.slack_automation_bot_button.id
  integration_type       = "AWS_PROXY"
  description            = "Lambda example"
  integration_method     = "POST"
  integration_uri        = aws_lambda_function.slack_automation_bot_button.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "slack_automation_bot_button" {
  api_id    = aws_apigatewayv2_api.slack_automation_bot_button.id
  route_key = "POST /slack/automation"
  target    = "integrations/${aws_apigatewayv2_integration.slack_automation_bot_button.id}"
}