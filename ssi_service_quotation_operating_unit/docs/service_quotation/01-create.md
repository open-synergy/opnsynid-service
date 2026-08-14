# Create Service Quotation

> **Module:** ssi_service_quotation_operating_unit\
> **Extends:** ssi_service_quotation — model `service.quotation`, aksi `01-create`

## Additional Fields

When this module is installed and the current company has multiple operating units
enabled (group `operating_unit.group_multi_operating_unit`), the create form gains one
field:

- **Operating Unit**: The operating unit the quotation belongs to. Not required.
  Defaults to the user's default operating unit; may be left as the default or changed
  by the user before Save.

## Modified — Record Visibility

- The quotation list is now filtered by operating unit (record rule). A user in group
  **Operating Unit** only sees quotations whose **Operating Unit** is one of the
  operating units assigned to them. This is not a Flow step.

## Additional Post-Condition

- When the quotation is won and a `service.contract` is generated from it
  (`_prepare_contract_data`), the created contract's **Operating Unit** is stamped with
  this quotation's own **Operating Unit**, instead of falling back to the acting user's
  own default operating unit. This is not a new Flow step; it only changes the Operating
  Unit recorded on the generated contract.
