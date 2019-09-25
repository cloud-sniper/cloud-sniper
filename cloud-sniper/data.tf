data "archive_file" "lambda_function_cloud_sniper" {
  type        = "zip"
  source_dir  = "./lambdas/functions/cloud-sniper/"
  output_path = "./lambdas/archives/lambda_function_cloud_sniper.zip"
}

data "aws_iam_policy_document" "iam_policy_document_kinesis_waf" {
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

data "aws_iam_policy_document" "iam_policy_lambda" {
  statement {
    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "iam_policy_firehose" {
  statement {
    principals {
      identifiers = ["firehose.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }
}

data "archive_file" "lambda_function_cloud_sniper_tagging" {
  type        = "zip"
  source_dir  = "./lambdas/functions/cloud-sniper-tagging/"
  output_path = "./lambdas/archives/lambda_function_cloud_sniper_tagging_ir.zip"
}
