# Cancel Service Contract

> **Module:** ssi_service\
> **Model:** `service.contract`\
> **Menu:** Service > Contracts\
> **Actor:** user in group `Service Contract - Validator`\
> **State:** `draft` | `confirm` | `open` | `done` | `terminate` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, **In Progress**, **Done**,
  or **Terminated**.
- **Config:** The `policy.template` grants `cancel_ok` for that state to the actor.
- **Access:** User is in group `Service Contract - Validator`.

## Flow

1. Open the **Service > Contracts** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
