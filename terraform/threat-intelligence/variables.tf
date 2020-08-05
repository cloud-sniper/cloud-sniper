//-------------------------------------------------------------------
// Cloud Sniper variables
//-------------------------------------------------------------------

variable "cloud_sniper_data_store" {
  default     = "cloud-sniper-data-store"
  description = " Cloud Sniper S3 data store"
}

variable "cloud_sniper_beaconing_findings_path" {
  default     = "/beaconing-detection/findings"
  description = "Cloud Sniper beaconing detection findings"
}

variable "cloud_sniper_beaconing_flows_path" {
  default     = "/beaconing-detection/vpc-flow-logs"
  description = "Cloud Sniper beaconing VPC flow logs path"
}

variable "cloud_sniper_iocs_path" {
  default     = "/iocs"
  description = "Cloud Sniper Indicators of Compromise"
}
