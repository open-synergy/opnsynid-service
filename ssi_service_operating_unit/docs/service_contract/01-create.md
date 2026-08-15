# Create Service Contract

> **Module:** ssi_service_operating_unit\
> **Extends:** ssi_service — model `service.contract`, aksi `01-create`

## Additional Fields

When this module is installed and the current company has multiple operating units
enabled (group `operating_unit.group_multi_operating_unit`), the create form gains one
field:

- **Operating Unit**: The operating unit the contract belongs to. Not required. Defaults
  to the user's default operating unit; may be left as the default or changed by the
  user before Save.

## Modified — Record Visibility

- The contract list is now filtered by operating unit (record rule). A user in group
  **Operating Unit** only sees contracts whose **Operating Unit** is one of the
  operating units assigned to them. This is not a Flow step.
