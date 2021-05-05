# slack automation

resource "aws_iam_role" "assume_role_slack_automation_bot" {
  name               = "slack-automation-bot"
  assume_role_policy = data.aws_iam_policy_document.policy_document_assume_slack_automation_bot.json
}

resource "aws_iam_policy" "policy_slack_automation_bot" {
  name   = "policy-slack-automation-bot"
  policy = data.aws_iam_policy_document.policy_document_slack_automation_bot.json
}

resource "aws_iam_role_policy_attachment" "iam_role_policy_attachment_slack_automation_bot" {
  role       = aws_iam_role.assume_role_slack_automation_bot.name
  policy_arn = aws_iam_policy.policy_slack_automation_bot.arn
}

# slack automation button

resource "aws_iam_role" "assume_role_slack_automation_bot_button" {
  name               = "slack-automation-bot-button"
  assume_role_policy = data.aws_iam_policy_document.policy_document_assume_slack_automation_bot_button.json
}

resource "aws_iam_policy" "policy_slack_automation_bot_button" {
  name   = "policy-slack-automation-bot-button"
  policy = data.aws_iam_policy_document.policy_document_slack_automation_bot_button.json
}

resource "aws_iam_role_policy_attachment" "iam_role_policy_attachment_slack_automation_bot_button" {
  role       = aws_iam_role.assume_role_slack_automation_bot_button.name
  policy_arn = aws_iam_policy.policy_slack_automation_bot_button.arn
}