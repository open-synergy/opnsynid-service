# Approve Service Contract

> **Module:** ssi_service_state_change_constrain\
> **Extends:** ssi_service — model `service.contract`, aksi `05-approve`

## Modified Validation

- Approve will fail with an error if a **State Change Constrain Template** applies to
  the resulting **In Progress** (`open`) status and the record has Status Check items
  required by that template whose **Status Ok** checkbox (on the **Status Checks** tab,
  see `01-create`) is not yet ticked. Whether a template applies at all is
  configuration-driven — it is only evaluated when **State Change Constrain Template**
  is set on the record.
