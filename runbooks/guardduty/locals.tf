locals {
  #your hub id
  invitation_message_guardduty = "Cloud Sniper GuardDuty account invitation"

  account_ids                = concat(list(local.hub_account_id), values(local.spoke_account_ids))
  current_account_first      = distinct(concat(list(data.aws_caller_identity.current.account_id), local.account_ids))
  account_ids_except_current = slice(local.current_account_first, 1, length(local.current_account_first))

  account_names                = keys(local.spoke_account_ids)
  current_name_first           = distinct(concat(list(local.hub_account_name), local.account_names))
  account_names_except_current = slice(local.current_name_first, 1, length(local.account_names))

  #customize
  hub_account_id   = "111111111111"
  hub_account_name = "hub-account-name"

  spoke_account_ids = {
    account-1 = "222222222222"
    account-b = "333333333333"
  }
}
