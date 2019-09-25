resource "aws_wafregional_web_acl" "acl-cloud-sniper" {
  name        = "acl-cloud-sniper"
  metric_name = "aclCloudSniper"

  default_action {
    type = "ALLOW"
  }

  rule {
    action {
      type = "BLOCK"
    }

    priority = 1
    rule_id  = "${aws_wafregional_rule.rule-cloud-sniper-country-blocked.id}"
    type     = "REGULAR"
  }

  rule {
    action {
      type = "BLOCK"
    }

    priority = 2
    rule_id  = "${aws_wafregional_rule.rule-cloud-sniper-automatic-ip-defense.id}"
    type     = "REGULAR"
  }

  logging_configuration {
    log_destination = "${aws_kinesis_firehose_delivery_stream.aws_waf_logs_cloudsniper.arn}"
  }
}

resource "aws_wafregional_rule" "rule-cloud-sniper-automatic-ip-defense" {
  depends_on  = ["aws_wafregional_ipset.ipset-cloud-sniper-automatic-block-these-ips"]
  name        = "rule-cloud-sniper-automatic-ip-defense"
  metric_name = "ruleCloudSniperAutomaticIpDefense"

  predicate {
    data_id = "${aws_wafregional_ipset.ipset-cloud-sniper-automatic-block-these-ips.id}"
    negated = false
    type    = "IPMatch"
  }
}

resource "aws_wafregional_rule" "rule-cloud-sniper-country-blocked" {
  depends_on  = ["aws_wafregional_geo_match_set.geo-match-set-cloud-sniper-country-blocked"]
  name        = "rule-cloud-sniper-country-blocked"
  metric_name = "ruleCloudSniperCountryBlocked"

  predicate {
    data_id = "${aws_wafregional_geo_match_set.geo-match-set-cloud-sniper-country-blocked.id}"
    negated = false
    type    = "GeoMatch"
  }
}

resource "aws_wafregional_geo_match_set" "geo-match-set-cloud-sniper-country-blocked" {
  name = "geo-match-set-cloud-sniper-country-blocked"

  geo_match_constraint {
    type  = "Country"
    value = "KP"
  }

  geo_match_constraint {
    type  = "Country"
    value = "HK"
  }

  geo_match_constraint {
    type  = "Country"
    value = "RU"
  }

  geo_match_constraint {
    type  = "Country"
    value = "SC"
  }

  geo_match_constraint {
    type  = "Country"
    value = "KZ"
  }

  geo_match_constraint {
    type  = "Country"
    value = "CN"
  }
}

resource "aws_wafregional_ipset" "ipset-cloud-sniper-automatic-block-these-ips" {
  name = "ipset-cloud-sniper-automatic-block-these-ips"
}
