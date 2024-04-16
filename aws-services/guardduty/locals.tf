locals {
  # Message for GuardDuty account invitation
  invitation_message_guardduty = "Cloud Sniper GuardDuty account invitation"

  # List of all account IDs
  account_ids = concat(list(local.hub_account_id), values(local.spoke_account_ids))
  
  # List of all account IDs with the current account ID at the first position
  current_account_first = distinct(concat(list(data.aws_caller_identity.current.account_id), local.account_ids))
  
  # List of all account IDs except the current account ID
  account_ids_except_current = slice(local.current_account_first, 1, length(local.current_account_first))

  # List of all account names
  account_names = keys(local.spoke_account_ids)
  
  # List of all account names with the hub account name at the first position
  current_name_first = distinct(concat(list(local.hub_account_name), local.account_names))
  
  # List of all account names except the hub account name
  account_names_except_current = slice(local.current_name_first, 1, length(local.account_names))

  # Hub account ID and name
  hub_account_id   = "${HUB_ACCOUNT_ID}"
  hub_account_name = "${HUB_ACCOUNT_NAME}"

  # Spoke account IDs
  spoke_account_ids = {
    account-1 = "${SPOKE_ACCOUNT_ID_1}"
    account-b = "${SPOKE_ACCOUNT_ID_2}"
  }
}
