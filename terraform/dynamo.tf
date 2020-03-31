resource "aws_dynamodb_table" "cloudsniper_table_ioc" {
  name = "cloudsniper-table-ioc"

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
