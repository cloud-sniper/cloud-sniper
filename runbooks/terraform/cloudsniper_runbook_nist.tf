resource "aws_config_config_rule" "iam-group-has-users-check" {
  name        = "iam-group-has-users-check"
  description = "Checks whether IAM groups have at least one IAM user"

  source {
    owner             = "AWS"
    source_identifier = "IAM_GROUP_HAS_USERS_CHECK"
  }
}

resource "aws_config_config_rule" "iam-user-group-membership-check" {
  name        = "iam-user-group-membership-check"
  description = "Checks whether IAM users are members of at least one IAM group"

  source {
    owner             = "AWS"
    source_identifier = "IAM_USER_GROUP_MEMBERSHIP_CHECK"
  }
}

resource "aws_config_config_rule" "iam-user-no-policies-check" {
  name        = "iam-user-no-policies-check"
  description = "Checks that none of the IAM users have policies attached. IAM users must inherit permissions from IAM groups or roles"

  source {
    owner             = "AWS"
    source_identifier = "IAM_USER_NO_POLICIES_CHECK"
  }
}

resource "aws_config_config_rule" "iam-user-unused-credentials-check" {
  name        = "iam-user-unused-credentials-check"
  description = "Checks whether your Identity and IAM users have passwords or active access keys that have not been used within the specified number of days you provided"

  source {
    owner             = "AWS"
    source_identifier = "IAM_USER_UNUSED_CREDENTIALS_CHECK"
  }

  input_parameters = <<EOF
  {
    "maxCredentialUsageAge": "90"
  }
  EOF
}

resource "aws_config_config_rule" "guardduty-enabled-centralized" {
  name        = "guardduty-enabled-centralized"
  description = "Checks whether GuardDuty is enabled in your account and region"

  source {
    owner             = "AWS"
    source_identifier = "GUARDDUTY_ENABLED_CENTRALIZED"
  }
}

resource "aws_config_config_rule" "vpc-default-security-group-closed" {
  name        = "vpc-default-security-group-closed"
  description = "Checks that the default security group of any VPC does not allow inbound or outbound traffic"

  source {
    owner             = "AWS"
    source_identifier = "VPC_DEFAULT_SECURITY_GROUP_CLOSED"
  }
}

resource "aws_config_config_rule" "acm-certificate-expiration-check" {
  name        = "acm-certificate-expiration-check"
  description = "Checks whether ACM Certificates in your account are marked for expiration within the specified number of days"

  source {
    owner             = "AWS"
    source_identifier = "ACM_CERTIFICATE_EXPIRATION_CHECK"
  }

  #21 days
}

resource "aws_config_config_rule" "access-keys-rotated" {
  name        = "access-keys-rotated"
  description = "Checks whether the active access keys are rotated within the number of days specified in maxAccessKeyAge"

  source {
    owner             = "AWS"
    source_identifier = "ACCESS_KEYS_ROTATED"
  }

  input_parameters = <<EOF
  {
    "maxAccessKeyAge": "90"
  }
  EOF
}

resource "aws_config_config_rule" "cloudtrail-enabled" {
  name        = "cloudtrail-enabled"
  description = "Checks whether CloudTrail is enabled in your account"

  source {
    owner             = "AWS"
    source_identifier = "CLOUD_TRAIL_ENABLED"
  }
}

resource "aws_config_config_rule" "cloud-trail-cloud-watch-logs-enabled" {
  name        = "cloud-trail-cloud-watch-logs-enabled"
  description = "Checks whether CloudTrail trails are configured to send logs to CloudWatch Logs"

  source {
    owner             = "AWS"
    source_identifier = "CLOUD_TRAIL_CLOUD_WATCH_LOGS_ENABLED"
  }
}

resource "aws_config_config_rule" "cloud-trail-encryption-enabled" {
  name        = "cloud-trail-encryption-enabled"
  description = "Checks whether CloudTrail is configured to use the server side encryption (SSE-KMS)"

  source {
    owner             = "AWS"
    source_identifier = "CLOUD_TRAIL_ENCRYPTION_ENABLED"
  }
}

resource "aws_config_config_rule" "cloud-trail-log-file-validation-enabled" {
  name        = "cloud-trail-log-file-validation-enabled"
  description = "Checks whether CloudTrail creates a signed digest file with logs"

  source {
    owner             = "AWS"
    source_identifier = "CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED"
  }
}

resource "aws_config_config_rule" "multi-region-cloud-trail-enabled" {
  name        = "multi-region-cloud-trail-enabled"
  description = "Checks that there is at least one multi-region CloudTrail"

  source {
    owner             = "AWS"
    source_identifier = "MULTI_REGION_CLOUD_TRAIL_ENABLED"
  }
}
