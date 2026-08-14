# Confirm Service Contract

> **Module:** ssi_service\
> **Model:** `service.contract`\
> **Menu:** Service > Contracts\
> **Actor:** user in group `Service Contract - User`\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** The `policy.template` grants `confirm_ok` for state `draft` to group
  `Service Contract - User`.
- **Config:** The `approval.template` for `service.contract` matches this record and has
  at least one approver level (group `Service Contract - Validator`).
- **Config:** The `sequence.template` for `service.contract` is active.
- **Access:** User is in group `Service Contract - User`.

## Flow

1. Open the **Service > Contracts** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for the approver level defined by the approval template
  (group `Service Contract - Validator`).
