variable "iam_indicators_path" {
  type        = string
  default     = "/iam"
  description = "Path for storing Indicators of Compromise (IOCs) related to IAM"
}

variable "data_store_bucket_name" {
  type        = string
  default     = "cloud-sniper-data-store"
  description = "Name of the S3 bucket used as a data store by Cloud Sniper"
}
