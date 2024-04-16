data "aws_caller_identity" "current" {}

data "aws_region" "current" {}


data "aws_iam_policy_document" "policy_document_assume_slack_automation_bot" {
  statement {
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }
}



data "aws_iam_policy_document" "policy_document_slack_automation_bot" {
  statement {
    effect = "Allow"

    actions = [
      "ec2:Describe*",
      "ec2:*NetworkAcl*",
      "ec2:DeleteNetworkInterface",
      "ec2:CreateNetworkInterface",
    ]

    resources = ["*"]
  }

  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = [
      "arn:aws:logs:*:*:*",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "secretsmanager:ListSecrets",
      "secretsmanager:GetSecretValue",
    ]

    resources = [
      aws_secretsmanager_secret.slack_automation_bot_secret.arn
    ]
  }
}

data "aws_iam_policy_document" "policy_document_assume_slack_automation_bot_button" {
  statement {
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }
}



data "aws_iam_policy_document" "policy_document_slack_automation_bot_button" {
  statement {
    effect = "Allow"

    actions = [
      "ec2:Describe*",
      "ec2:*NetworkAcl*",
      "ec2:DeleteNetworkInterface",
      "ec2:CreateNetworkInterface",
    ]

    resources = ["*"]
  }

  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = [
      "arn:aws:logs:*:*:*",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "secretsmanager:ListSecrets",
      "secretsmanager:GetSecretValue",
    ]

    resources = [
      aws_secretsmanager_secret.slack_automation_bot_secret.arn
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:Query",
      "dynamodb:Scan",
      "dynamodb:UpdateItem",
    ]

    resources = [
      "arn:aws:dynamodb:${local.region}:${local.main_account_id}:table/${local.dynamodb_name}"
    ]
  }
}

data "archive_file" "slack_automation_bot" {
  type        = "zip"
  source_dir  = "${path.module}/lambdas/python/slack_automation_bot/"
  output_path = "${path.module}/lambdas/archive/slack_automation_bot.zip"
}