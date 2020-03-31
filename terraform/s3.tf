resource "aws_s3_bucket" "cloudsniper_s3_bucket_data_store" {
  bucket = "${var.cloudsniper_data_store}"
  acl    = "private"
}
