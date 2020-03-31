resource "aws_wafregional_web_acl" "cloudsniper-wafregional-acl" {
  name        = "cloudsniper-wafregional-acl"
  metric_name = "cloudsniperacl"

  default_action {
    type = "ALLOW"
  }

  rule {
    action {
      type = "BLOCK"
    }

    priority = 1
    rule_id  = "${aws_wafregional_rule.cloudsniper-wafregional-rule-country-blacklist.id}"
    type     = "REGULAR"
  }

  rule {
    action {
      type = "BLOCK"
    }

    priority = 2
    rule_id  = "${aws_wafregional_rule.cloudsniper-wafregional-rule-ips-blacklist.id}"
    type     = "REGULAR"
  }

  logging_configuration {
    log_destination = "${aws_kinesis_firehose_delivery_stream.cloudsniper_aws_waf_logs.arn}"
  }
}

resource "aws_wafregional_rule" "cloudsniper-wafregional-rule-ips-blacklist" {
  depends_on  = ["aws_wafregional_ipset.cloudsniper-wafregional-ipset-automatic-block-these-ips"]
  name        = "cloudsniper-wafregional-rule-ips-blacklist"
  metric_name = "cloudsniperipsblacklist"

  predicate {
    data_id = "${aws_wafregional_ipset.cloudsniper-wafregional-ipset-automatic-block-these-ips.id}"
    negated = false
    type    = "IPMatch"
  }
}

resource "aws_wafregional_rule" "cloudsniper-wafregional-rule-country-blacklist" {
  depends_on  = ["aws_wafregional_geo_match_set.cloudsniper-wafregional-geo-match-set-country-blacklist"]
  name        = "cloudsniper-wafregional-rule-country-blacklist"
  metric_name = "cloudsnipercountryblacklist"

  predicate {
    data_id = "${aws_wafregional_geo_match_set.cloudsniper-wafregional-geo-match-set-country-blacklist.id}"
    negated = false
    type    = "GeoMatch"
  }
}

resource "aws_wafregional_geo_match_set" "cloudsniper-wafregional-geo-match-set-country-blacklist" {
  name = "cloudsniper-geo-match-set-country-blacklist"

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

resource "aws_wafregional_ipset" "cloudsniper-wafregional-ipset-automatic-block-these-ips" {
  name = "cloudsniper-wafregional-ipset-block-these-ips"
}
