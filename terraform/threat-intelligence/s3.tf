resource "aws_s3_bucket" "cloud_sniper_s3_bucket_data_store" {
  bucket = var.cloud_sniper_data_store
  acl    = "private"
}
