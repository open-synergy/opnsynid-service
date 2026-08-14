# Confirm Service Quotation

> **Module:** ssi_service_quotation\
> **Model:** `service.quotation`\
> **Menu:** Service > Quotations\
> **Actor:** user in group `Service Quotation - User`\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** The `policy.template` grants `confirm_ok` for state `draft` to group
  `Service Quotation - User`.
- **Config:** The `approval.template` for `service.quotation` matches this record and
  has at least one approver level (group `Service Quotation - Validator`).
- **Config:** The `sequence.template` for `service.quotation` is active.
- **Access:** User is in group `Service Quotation - User`.

## Flow

1. Open the **Service > Quotations** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for the approver level defined by the approval template
  (group `Service Quotation - Validator`).
