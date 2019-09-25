data "aws_iam_policy_document" "iam_policy_document_cloud_sniper" {
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

resource "aws_iam_policy" "iam_policy_cloud_sniper" {
  name        = "iam_policy_cloud_sniper"
  path        = "/"
  description = "iam_policy_cloud_sniper"
  policy      = "${data.aws_iam_policy_document.iam_policy_document_cloud_sniper.json}"
}

data "aws_iam_policy_document" "iam_policy_document_cloud_sniper_tagging_sniffer" {
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

resource "aws_iam_policy" "iam_policy_cloud_sniper_tagging_sniffer" {
  name        = "iam_policy_cloud_sniper_tagging_sniffer"
  path        = "/"
  description = "iam_policy_cloud_sniper_tagging_sniffer"
  policy      = "${data.aws_iam_policy_document.iam_policy_document_cloud_sniper_tagging_sniffer.json}"
}

data "aws_iam_policy_document" "iam_policy_document_cloud_sniper_tagging_incident_and_response" {
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

resource "aws_iam_policy" "iam_policy_cloud_sniper_tagging_incident_and_response" {
  name        = "iam_policy_cloud_sniper_tagging_incident_and_response"
  path        = "/"
  description = "iam_policy_cloud_sniper_tagging_incident_and_response"
  policy      = "${data.aws_iam_policy_document.iam_policy_document_cloud_sniper_tagging_incident_and_response.json}"
}
