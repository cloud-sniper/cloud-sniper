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

# Customize
variable "cloud_sniper_hub_account_id" {
  default     = "[account-id]"
  description = " Cloud Sniper hub account id"
  sensitive   = true
}

variable "cloud_sniper_slack_webhook" {
  default     = "[https://hooks.slack.com/services/xxxx]"
  description = " Cloud Sniper Slack webhook"
  sensitive   = true
}
