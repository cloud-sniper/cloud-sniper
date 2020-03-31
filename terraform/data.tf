data "aws_iam_policy_document" "cloudsniper_policy_document" {
  statement {
    effect = "Allow"

    actions = [
      "waf-regional:GetIPSet",
      "waf-regional:UpdateIPSet",
      "waf-regional:GetChangeToken",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "kms:*",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "ec2:Describe*",
      "ec2:*NetworkAcl*",
    ]

    resources = [
      "*",
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
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:Query",
      "dynamodb:Scan",
      "dynamodb:DeleteItem",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "sqs:*",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "s3:*",
    ]

    resources = [
      "*",
    ]
  }
}

data "aws_iam_policy_document" "cloudsniper_policy_document_tagging" {
  statement {
    effect = "Allow"

    actions = [
      "cloudtrail:LookupEvents",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "ec2:CreateTags",
      "ec2:Describe*",
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = [
      "*",
    ]
  }
}

data "aws_iam_policy_document" "cloudsniper_policy_document_tagging_incident_and_response" {
  statement {
    effect = "Allow"

    actions = [
      "ec2:Describe*",
      "ec2:RunInstances",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "ec2:StopInstances",
      "ec2:StartInstances",
      "ec2:RebootInstances",
      "ec2:TerminateInstances",
    ]

    resources = [
      "*",
    ]

    condition {
      test     = "StringEquals"
      variable = "ec2:ResourceTag/PrincipalId"

      values = [
        "&{aws:userid}",
      ]
    }
  }
}

data "aws_iam_policy_document" "cloudsniper_policy_document_assume" {
  statement {
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "cloudsniper_policy_firehose" {
  statement {
    principals {
      identifiers = ["firehose.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "cloudsniper_policy_document_kinesis_waf" {
  statement {
    resources = ["*"]

    actions = [
      "ec2:Describe*",
      "firehose:DeleteDeliveryStream",
      "firehose:PutRecord",
      "firehose:PutRecordBatch",
      "firehose:UpdateDestination",
      "s3:*",
    ]
  }
}

data "archive_file" "cloudsniper_archive_file_lambda_ir" {
  type        = "zip"
  source_dir  = "./lambdas/functions/cloud-sniper/"
  output_path = "./lambdas/archives/lambda_function_cloud_sniper.zip"
}

data "archive_file" "cloudsniper_archive_file_lambda_tagging_ir" {
  type        = "zip"
  source_dir  = "./lambdas/functions/cloud-sniper-tagging/"
  output_path = "./lambdas/archives/lambda_function_cloud_sniper_tagging_ir.zip"
}
