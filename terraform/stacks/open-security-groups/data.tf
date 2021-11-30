data "aws_caller_identity" "current" {}

data "aws_region" "current" {}


data "aws_iam_policy_document" "assume_open_security_group_automation" {
  statement {
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "open_security_group_automation" {
  statement {
    effect = "Allow"

    actions = [
      "ec2:DescribeNetworkInterfaces",
      "ec2:DescribeInstances",
      "ec2:CreateNetworkInterface",
      "ec2:DeleteNetworkInterface",
      "ec2:DescribeSecurityGroups",
      "ec2:DescribeSecurityGroupReferences",
      "ec2:DescribeStaleSecurityGroups",
      "ec2:DescribeVpcs",
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
      "s3:ListBucket",
      "s3:ListObjects",
    ]

    resources = [
      "arn:aws:s3:::${local.ir_data_store}",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:GetObject",
    ]

    resources = [
      "arn:aws:s3:::${local.ir_data_store}",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "ec2:AuthorizeSecurityGroupEgress",
      "ec2:AuthorizeSecurityGroupIngress",
      "ec2:RevokeSecurityGroupEgress",
      "ec2:RevokeSecurityGroupIngress",
    ]

    resources = ["arn:aws:ec2:*:*:security-group/*"]
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
      aws_dynamodb_table.table_security_automated_actions.arn
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "lambda:InvokeFunction",
    ]

    resources = [
      local.bot_lambda_arn
    ]
  }

}

data "archive_file" "open_security_groups_automation" {
  type        = "zip"
  source_dir  = "${path.module}/lambdas/python/open_security_group/"
  output_path = "${path.module}/lambdas/archive/open_security_group.zip"
}