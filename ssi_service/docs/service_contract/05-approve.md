# Approve Service Contract

> **Module:** ssi_service\
> **Model:** `service.contract`\
> **Menu:** Service > Contracts\
> **Actor:** user in group `Service Contract - Validator`\
> **State:** `confirm` → `open`\
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** The `policy.template` grants `approve_ok` to the actor.
- **Access:** User is registered as an approver on the pending approval level (group
  `Service Contract - Validator`).

## Flow

1. Open the **Service > Contracts** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Since the approval template defines a single approver level, the contract status
  changes directly to **In Progress** (`open`) once that level is approved — there is no
  separate manual "Start" step.
- The contract's document number is assigned according to the sequence template.
- An analytic account is automatically created (or refreshed, if one already exists) and
  linked to **Analytic Account** on the **Analytic & Project** tab.
