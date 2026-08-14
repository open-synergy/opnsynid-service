# Approve Service Quotation

> **Module:** ssi_service_quotation\
> **Model:** `service.quotation`\
> **Menu:** Service > Quotations\
> **Actor:** user in group `Service Quotation - Validator`\
> **State:** `confirm` → `open`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** The `policy.template` grants `approve_ok` to the actor.
- **Access:** User is registered as an approver on the pending approval level (group
  `Service Quotation - Validator`).

## Flow

1. Open the **Service > Quotations** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Since the approval template defines a single approver level, the quotation status
  changes directly to **In Progress** (`open`) once that level is approved — there is no
  separate manual "Start" step.
- The quotation's document number is assigned according to the sequence template.
