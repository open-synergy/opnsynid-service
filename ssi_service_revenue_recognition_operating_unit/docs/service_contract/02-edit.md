# Edit Service Contract

> **Module:** ssi_service_revenue_recognition_operating_unit\
> **Extends:** ssi_service_revenue_recognition — model `service.contract`, aksi `02-edit`

## Additional Post-Condition

- When the **Create PoB** gear-icon button (`action_create_pob`, documented as an Inline
  Action on `ssi_service_revenue_recognition`'s `02-edit.md`) creates a new Performance
  Obligation, that Performance Obligation's **Operating Unit** is now stamped with this
  contract's own **Operating Unit** (the field added by `ssi_service_operating_unit`,
  `service_id.operating_unit_id`), instead of falling back to the acting user's own
  default Operating Unit. This is not a new Flow step — clicking the button still
  behaves exactly as documented in the base module; only the Operating Unit recorded on
  the created Performance Obligation changes.
