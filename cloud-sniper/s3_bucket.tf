resource "aws_s3_bucket" "s3_bucket_cloud_sniper_data_store" {
  bucket = "${var.cloud_sniper_data_store}"
  acl    = "private"
}
