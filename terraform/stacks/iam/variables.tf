//-------------------------------------------------------------------
// Cloud Sniper variables
//-------------------------------------------------------------------

variable "cloud_sniper_iam_path" {
  default     = "/iam"
  description = "Cloud Sniper Indicators of Compromise"
}

variable "cloud_sniper_data_store" {
  default     = "cloud-sniper-data-store"
  description = " Cloud Sniper S3 data store"
}
