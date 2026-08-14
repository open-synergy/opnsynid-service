# Mark Service Quotation as Lost

> **Module:** ssi_service_quotation\
> **Model:** `service.quotation`\
> **Menu:** Service > Quotations\
> **Actor:** user in group `Service Quotation - User`\
> **State:** `open` → `lost`\
> **Requires:** `05-approve`

## Pre-Condition

- **Record:** Status is **In Progress** (`open`).
- **Config:** The `policy.template` grants `lost_ok` to the actor.
- **Data:** At least one `base.lost_reason` record exists and is enabled for this
  quotation's company (shipped with Odoo core CRM).
- **Access:** User is in group `Service Quotation - User`.

## Flow

1. Open the **Service > Quotations** menu.
2. Open the record to mark as lost.
3. Click the **Lost** button.
4. In the wizard that appears, select the **Lost Reason**.
5. Click **Confirm**.

## Post-Condition

- Status changes to **Lost**.
- **Lost Reason** on the quotation is set to the reason selected in the wizard.
