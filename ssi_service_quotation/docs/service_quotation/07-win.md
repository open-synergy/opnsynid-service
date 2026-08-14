# Mark Service Quotation as Win

> **Module:** ssi_service_quotation\
> **Model:** `service.quotation`\
> **Menu:** Service > Quotations\
> **Actor:** user in group `Service Quotation - User`\
> **State:** `open` → `win`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **In Progress** (`open`).
- **Config:** The `policy.template` grants `win_ok` to the actor.
- **Access:** User is in group `Service Quotation - User`.

## Flow

1. Open the **Service > Quotations** menu.
2. Open the record to mark as win.
3. Click the **Win** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Win**.
- A new **Service Contract** is automatically created from the quotation's data
  (partner, type, payment terms, and their detail lines) and linked to the quotation's
  **# Contract** field.
