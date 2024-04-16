resource "aws_s3_bucket" "cloud_sniper_s3_bucket_data_store" {
  for_each = local.hub_account_id == data.aws_caller_identity.current.account_id ? { hub : true } : {}
  bucket   = join("-", [var.cloud_sniper_data_store, data.aws_region.current.name])
}

resource "aws_s3_bucket_public_access_block" "cloud_sniper_s3_bucket_access_block" {
  bucket                  = aws_s3_bucket.cloud_sniper_s3_bucket_data_store["hub"].id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "cloud_sniper_beaconing_file_upload" {
  for_each = local.hub_account_id == data.aws_caller_identity.current.account_id ? { hub : true } : {}
  bucket   = aws_s3_bucket.cloud_sniper_s3_bucket_data_store["hub"].id
  key      = "cloud_sniper_beaconing_detection.zip"
  source   = "../analytics/target/cloud_sniper_beaconing_detection.zip"
}
