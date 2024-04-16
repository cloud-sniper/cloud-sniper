resource "aws_dynamodb_table" "cloud_sniper_table" {
  for_each = local.is_hub_account ? { hub : true } : {}

  name           = "table-security-ir-automation"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "attacker_ip"

  attribute {
    name = "attacker_ip"
    type = "S"
  }

  tags = local.cloud_sniper_tags
}
