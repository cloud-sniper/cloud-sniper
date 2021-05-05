data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_iam_policy_document" "cloud_sniper_policy_document_assume_lusat" {
  statement {
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }

}

data "aws_iam_policy_document" "cloud_sniper_policy_document_lusat" {
  statement {
    effect = "Allow"

    actions = [
      "ec2:DescribeNetworkInterfaces",
      "ec2:DescribeInstances",
      "ec2:CreateNetworkInterface",
      "ec2:DeleteNetworkInterface",
      "ec2:Describe*",
      "ec2:*NetworkAcl*",
      "iam:ListAccountAliases",
      "rds:DescribeDBInstances",
      "elasticloadbalancing:Describe*",
      "rds:DescribeDBSecurityGroups",
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
      "arn:aws:s3:::${var.cloud_sniper_data_store}",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]

    resources = [
      "arn:aws:s3:::${var.cloud_sniper_data_store}/*",
    ]
  }
}

data "archive_file" "cloud_sniper_lambda_lusat" {
  type        = "zip"
  source_dir  = "${path.module}/lambdas/python/lusat/"
  output_path = "${path.module}/lambdas/archive/lusat.zip"
}
