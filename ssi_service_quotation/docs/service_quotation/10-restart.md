# Restart Service Quotation

> **Module:** ssi_service_quotation\
> **Model:** `service.quotation`\
> **Menu:** Service > Quotations\
> **Actor:** user in group `Service Quotation - Validator`\
> **State:** `cancel` | `reject` → `draft`\
> **Requires:** `09-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled** or **Rejected**.
- **Config:** The `policy.template` grants `restart_ok` for that state to the actor.
- **Access:** User is in group `Service Quotation - Validator`.

## Flow

1. Open the **Service > Quotations** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
- All approval records are removed and the approval template is cleared. A later Confirm
  starts the approval process from the beginning.
