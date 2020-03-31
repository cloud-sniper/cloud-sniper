resource "aws_lambda_function" "cloudsniper_lambda_function_ir" {
  function_name    = "cloudsniper-lambda-function"
  handler          = "cloud_sniper.cloud_sniper"
  memory_size      = 1024
  timeout          = 300
  role             = "${aws_iam_role.cloudsniper_role.arn}"
  runtime          = "python3.6"
  filename         = "${data.archive_file.cloudsniper_archive_file_lambda_ir.output_path}"
  source_code_hash = "${data.archive_file.cloudsniper_archive_file_lambda_ir.output_base64sha256}"

  environment {
    variables {
      DYNAMO_TABLE_CLOUD_SNIPER = "${aws_dynamodb_table.cloudsniper_table_ioc.name}"
    }

    variables {
      CLOUDSNIPER-WAFREGIONAL-IPSET-BLOCK-THESE-IP = "${aws_wafregional_ipset.cloudsniper-wafregional-ipset-automatic-block-these-ips.id}"
    }

    variables {
      SQS_QUEUE_CLOUD_SNIPER = "${aws_sqs_queue.cloudsniper_sqs_queue.id}"
    }

    variables {
      BUCKET_CLOUD_SNIPER = "${aws_s3_bucket.cloudsniper_s3_bucket_data_store.id}"
    }
  }
}

resource "aws_lambda_function" "cloudsniper_lambda_function_tagging_ir" {
  function_name    = "cloudsniper-lambda-function-tagging-ir"
  handler          = "cloud_sniper_tagging_ir.cloud_sniper_tagging_ir"
  memory_size      = 1024
  timeout          = 300
  role             = "${aws_iam_role.cloudsniper_role_tagging.arn}"
  runtime          = "python3.6"
  filename         = "${data.archive_file.cloudsniper_archive_file_lambda_tagging_ir.output_path}"
  source_code_hash = "${data.archive_file.cloudsniper_archive_file_lambda_tagging_ir.output_base64sha256}"
}

resource "aws_lambda_permission" "cloudsniper_lambda_permission_ir" {
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.cloudsniper_lambda_function_ir.function_name}"
  principal     = "events.amazonaws.com"
}

resource "aws_lambda_permission" "cloudsniper_lambda_permission_tagging_ir" {
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.cloudsniper_lambda_function_tagging_ir.function_name}"
  principal     = "events.amazonaws.com"
}
