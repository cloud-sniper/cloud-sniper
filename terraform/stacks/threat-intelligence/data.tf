data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_iam_policy_document" "cloud_sniper_policy_document_assume_spoke_threat_intelligence_automation" {
  statement {
    principals {
      identifiers = ["arn:aws:iam::${local.hub_account_id}:role/${format("%s-%s", local.cloud_sniper_assume_role_threat_intelligence_automation, data.aws_region.current.name)}"]
      type        = "AWS"
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "cloud_sniper_policy_document_spoke_threat_intelligence_automation" {
  statement {
    effect = "Allow"

    actions = [
      "ec2:Describe*",
      "ec2:*NetworkAcl*",
      "iam:ListAccountAliases",
    ]

    resources = ["*"]
  }
}

data "aws_iam_policy_document" "cloud_sniper_policy_document_threat_intelligence_automation" {

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
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:Query",
      "dynamodb:Scan",
      "dynamodb:DeleteItem",
      "dynamodb:UpdateItem",
    ]

    resources = [
      "arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:table/${aws_dynamodb_table.cloud_sniper_table["hub"].name}",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "sqs:*",
    ]

    resources = [
      "arn:aws:sqs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${join("-", ["cloud-sniper-sqs-queue-threat-intelligence-automation", data.aws_region.current.name])}",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "sns:Publish",
    ]

    resources = [
      "arn:aws:sns:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${aws_sns_topic.cloud_sniper_sns_topic_threat_intelligence["hub"].name}",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "iam:ListAccountAliases",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "s3:ListBucket",
      "s3:ListObjects",
    ]

    resources = [
      "arn:aws:s3:::${join("-", [var.cloud_sniper_data_store, data.aws_region.current.name])}",
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
      "arn:aws:s3:::${join("-", [var.cloud_sniper_data_store, data.aws_region.current.name])}/*",
    ]
  }
}

data "aws_iam_policy_document" "cloud_sniper_policy_document_assume_threat_intelligence_automation" {
  statement {
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }
}

data "archive_file" "cloud_sniper_archive_threat_intelligence_automation" {
  type        = "zip"
  source_dir  = "${path.module}/lambdas/python/cloud-sniper-threat-intelligence/"
  output_path = "${path.module}/lambdas/archives/cloud-sniper-threat-intelligence.zip"
}

## Analytics
data "aws_iam_policy_document" "cloud_sniper_policy_document_assume_beaconing_detection" {
  statement {
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "cloud_sniper_policy_document_beaconing_detection" {
  statement {
    effect = "Allow"

    actions = [
      "s3:ListBucket",
      "s3:ListObjects",
    ]

    resources = [
      "arn:aws:s3:::${aws_s3_bucket.cloud_sniper_s3_bucket_data_store["hub"].id}",
    ]
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
      "s3:GetObject",
      "s3:PutObject",
    ]

    resources = [
      "arn:aws:s3:::${aws_s3_bucket.cloud_sniper_s3_bucket_data_store["hub"].id}/*",
    ]
  }
}
