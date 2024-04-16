locals {

  cloud_sniper_tags = {
    Owner      = "Cloud Sniper"
    Department = "engineering"
    Purpose    = "Cloud Sniper - Automated Actions - Open Security Groups"
    TagVersion = "1.0"
  }

  region = "us-west-2"

  dynamodb_name = "cloud-sniper-automated-actions"

  bot_lambda_arn = "" # your lambda bot ARN

  bot_lambda_name = "" # your lambda bot NAME

  ir_data_store = "" # your data store NAME

}