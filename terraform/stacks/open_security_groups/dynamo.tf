resource "aws_dynamodb_table" "table_security_automated_actions" {
  name           = local.dynamodb_name
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "ID"

  attribute {
    name = "ID"
    type = "S"
  }

  tags = local.cloud_sniper_tags
}
