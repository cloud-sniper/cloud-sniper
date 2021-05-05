resource "aws_lambda_function" "cloud_sniper_lambda_lusat" {
  function_name    = "cloud-sniper-lambda-lusat"
  description      = "Cloud Sniper - Cloud Lusat - Security Inventory"
  handler          = "lusat.handler"
  memory_size      = "1024"
  timeout          = "300"
  runtime          = "python3.6"
  filename         = data.archive_file.cloud_sniper_lambda_lusat.output_path
  source_code_hash = data.archive_file.cloud_sniper_lambda_lusat.output_base64sha256
  role             = aws_iam_role.cloud_sniper_assume_role_lusat.arn

  environment {
    variables = {
      BUCKET_NAME                   = var.cloud_sniper_data_store
      LUSAT_PATH                    = var.cloud_sniper_lusat_path
    }
  }

  tags = local.cloud_sniper_tags
}
