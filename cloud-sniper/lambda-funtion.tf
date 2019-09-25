resource "aws_lambda_function" "lambda_function_cloud_sniper" {
  function_name    = "lambda_function_cloud_sniper"
  description      = "lambda_function_cloud_sniper"
  handler          = "cloud_sniper.cloud_sniper"
  memory_size      = 1024
  timeout          = 300
  role             = "${aws_iam_role.role_cloud_sniper.arn}"
  runtime          = "python3.7"
  filename         = "${data.archive_file.lambda_function_cloud_sniper.output_path}"
  source_code_hash = "${data.archive_file.lambda_function_cloud_sniper.output_base64sha256}"

  environment {
    variables {
      DYNAMO_TABLE_CLOUD_SNIPER = "${aws_dynamodb_table.dynamo_table_cloud_sniper.name}"
    }

    variables {
      IPSET_CLOUD_SNIPER_AUTOMATIC_BLOCK_THESE_IPS = "${aws_wafregional_ipset.ipset-cloud-sniper-automatic-block-these-ips.id}"
    }

    variables {
      SQS_QUEUE_CLOUD_SNIPER = "${aws_sqs_queue.sqs_queue_cloud_sniper.id}"
    }

    variables {
      BUCKET_CLOUD_SNIPER = "${aws_s3_bucket.s3_bucket_cloud_sniper_data_store.id}"
    }
  }
}

resource "aws_lambda_function" "lambda_function_cloud_sniper_tagging_ir" {
  function_name    = "lambda_function_cloud_sniper_tagging_incident_and_response"
  description      = "lambda_function_cloud_sniper_tagging_incident_and_response"
  handler          = "cloud_sniper_tagging_ir.cloud_sniper_tagging_ir"
  memory_size      = 1024
  timeout          = 300
  role             = "${aws_iam_role.role_cloud_sniper_tagging.arn}"
  runtime          = "python3.7"
  filename         = "${data.archive_file.lambda_function_cloud_sniper_tagging.output_path}"
  source_code_hash = "${data.archive_file.lambda_function_cloud_sniper_tagging.output_base64sha256}"
}
