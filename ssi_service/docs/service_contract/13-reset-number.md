# Reset Document Number — Service Contract

> **Module:** ssi_service\
> **Model:** `service.contract`\
> **Menu:** Service > Contracts\
> **Actor:** user in group `Service Contract - Validator`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** The `sequence.template` for `service.contract` is active.
- **Access:** User is in group `Service Contract - Validator`.

## Flow

1. Open the **Service > Contracts** menu.
2. Open the record whose document number will be reset.
3. Click the **Reset Document Number** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Document number returns to **/**.
- The record will receive an automatic number when it transitions to **In Progress**
  (`open`), according to the sequence template configuration.
