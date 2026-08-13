# Reject Service Contract

> **Module:** ssi_service\
> **Model:** `service.contract`\
> **Menu:** Service > Contracts\
> **Actor:** user in group `Service Contract - Validator`\
> **State:** `confirm` → `reject`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** The `policy.template` grants `reject_ok` to the actor.
- **Access:** User is registered as an approver on the pending approval level (group
  `Service Contract - Validator`).

## Flow

1. Open the **Service > Contracts** menu.
2. Open the record to reject.
3. Click the **Reject** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Rejected**.
