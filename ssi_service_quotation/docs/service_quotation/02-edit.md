# Edit Service Quotation

> **Module:** ssi_service_quotation\
> **Model:** `service.quotation`\
> **Menu:** Service > Quotations\
> **Actor:** user in group `Service Quotation - User`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group `Service Quotation - User`.

## Flow

1. Open the **Service > Quotations** menu.
2. Find and open the record to edit.
3. Change any of the fields described in `01-create`.
4. On the **Fix Item** tab, add, change, or remove **Payment Terms** lines and their
   **Details** sub-lines as needed.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
