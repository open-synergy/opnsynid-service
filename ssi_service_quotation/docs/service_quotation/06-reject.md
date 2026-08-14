# Reject Service Quotation

> **Module:** ssi_service_quotation\
> **Model:** `service.quotation`\
> **Menu:** Service > Quotations\
> **Actor:** user in group `Service Quotation - Validator`\
> **State:** `confirm` → `reject`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** The `policy.template` grants `reject_ok` to the actor.
- **Access:** User is registered as an approver on the pending approval level (group
  `Service Quotation - Validator`).

## Flow

1. Open the **Service > Quotations** menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
