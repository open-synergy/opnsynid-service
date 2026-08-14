# Cancel Service Quotation

> **Module:** ssi_service_quotation\
> **Model:** `service.quotation`\
> **Menu:** Service > Quotations\
> **Actor:** user in group `Service Quotation - Validator`\
> **State:** `draft` | `confirm` | `open` | `win` | `lost` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, **In Progress**, **Win**,
  or **Lost**.
- **Config:** The `policy.template` grants `cancel_ok` for that state to the actor.
- **Access:** User is in group `Service Quotation - Validator`.

## Flow

1. Open the **Service > Quotations** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- If the quotation had a linked **Service Contract** (set when it was marked as
  **Win**), that contract is also cancelled with the same reason and the quotation's **#
  Contract** field is cleared.
