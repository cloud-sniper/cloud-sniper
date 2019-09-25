resource "aws_dynamodb_table" "dynamo_table_cloud_sniper" {
  name = "dynamo_table_cloud_sniper"

  read_capacity  = 5
  write_capacity = 5
  hash_key       = "ip_attacker"
  range_key      = "timestamp"

  attribute {
    name = "timestamp"
    type = "S"
  }

  attribute {
    name = "ip_attacker"
    type = "S"
  }
}
