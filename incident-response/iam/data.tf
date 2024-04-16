data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_iam_policy_document" "cloud_sniper_policy_document_spoke_assume_iam_automation" {
  statement {
    principals {
      identifiers = ["arn:aws:iam::${local.hub_account_id}:role/${format("%s-%s", local.cloud_sniper_role_hub_iam_automation, data.aws_region.current.name)}"]
      type        = "AWS"
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "cloud_sniper_policy_document_spoke_iam_automation" {
  statement {
    effect = "Allow"

    actions = [
      "iam:ListUsers",
      "iam:ListAccessKeys",
      "iam:GetAccessKeyLastUsed",
      "config:ListDiscoveredResources",
    ]

    resources = ["*"]
  }
}

data "aws_iam_policy_document" "cloud_sniper_policy_document_assume_iam_automation" {
  statement {
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "cloud_sniper_policy_document_iam_automation" {
  statement {
    effect = "Allow"

    actions = [
      "iam:ListUsers",
      "iam:ListAccessKeys",
      "iam:GetAccessKeyLastUsed",
      "config:ListDiscoveredResources",
      "config:GetAggregateComplianceDetailsByConfigRule",
      "ec2:DescribeNetworkInterfaces",
      "ec2:DescribeInstances",
      "ec2:CreateNetworkInterface",
      "ec2:DeleteNetworkInterface",
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
      "arn:aws:s3:::${local.cloud_sniper_data_store}",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]

    resources = [
      "arn:aws:s3:::${local.cloud_sniper_data_store}/*",
    ]
  }
}

data "archive_file" "cloud_sniper_lambda_iam_automation" {
  type        = "zip"
  source_dir  = "${path.module}/lambdas/python/cloud_sniper_iam/"
  output_path = "${path.module}/lambdas/archive/cloud_sniper_iam.zip"
}
