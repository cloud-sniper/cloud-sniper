# Whether to enable GuardDuty
variable "enable" {
  description = "Whether to enable GuardDuty"
  default     = true
}

# The domain for the email addresses of the GuardDuty members
variable "email_domain" {
  description = "The domain for the email addresses of the GuardDuty members"
  default     = "domain.com"
}
