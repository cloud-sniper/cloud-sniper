resource "aws_dynamodb_table" "cloud_sniper_table_ioc" {
  for_each            = { "hub" = local.hub_account_id } == { "hub" = data.aws_caller_identity.current.account_id } ? { hub : true } : {}
  name = "cloud-sniper-table-ioc"

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
