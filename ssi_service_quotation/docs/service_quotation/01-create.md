# Create Service Quotation

> **Module:** ssi_service_quotation\
> **Model:** `service.quotation`\
> **Menu:** Service > Quotations\
> **Actor:** user in group `Service Quotation - User`\
> **State:** `—` → `draft`\
> **Inline Actions:** `%(copy_quotation_term_action)d` (Copy Term), `action_recompute_price`
> (Recompute Price)

## Pre-Condition

- **Config:** An active `policy.template` for `service.quotation` is installed (shipped
  with the module).
- **Config:** An active `sequence.template` for `service.quotation` is installed
  (shipped with the module).
- **Data:** A `service.type` record exists (see `service.type` master data).
- **Data:** A `res.partner` record exists to use as the quotation's **Partner**.
- **Access:** User is in group `Service Quotation - User`.

## Flow

1. Open the **Service > Quotations** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Title** _(required)_: Free-text title of the quotation.
   - **Partner** _(required)_: The customer this quotation is for.
   - **Contact**: Optional. Domain-filtered to contacts of the selected Partner.
   - **Sale Team**: Optional.
   - **Salesperson** _(required)_.
   - **Contractor**: Optional.
   - **Contact's Contractor**: Optional. Domain-filtered to contacts of the selected
     Contractor.
   - **Type** _(required)_: The `service.type` that governs allowed products and
     pricelists.
   - **Manager** _(required)_: The user responsible for the quotation.
   - **Date** _(required)_: Reference date used by the document sequence.
   - **Date Start** / **Date End** _(required)_: The quoted period.
   - **Currency** _(required)_.
   - **Pricelist** _(required)_: Domain-filtered to pricelists allowed by **Type** and
     matching **Currency**.
4. On the **Fix Item** tab, under **Payment Terms**, click **Add a line** to add at
   least one payment term. Repeat as many times as needed:
   - **Term**: Name of the payment term line.
   - Under the term's **Details** sub-table, click **Add a line** to add each product
     line. Repeat as many times as needed:
     - **Product**: Domain-filtered to products/categories allowed by **Type**.
     - **Description**, **Account**, **Quantity**, **UoM**, **Price Unit**, **Taxes**.
   - Click the row's **Copy Term** button to duplicate an existing payment term (its
     name, sequence, and detail lines) into a new line instead of building one from
     scratch. In the wizard that appears, fill in the new **Term** name and
     **Sequence**, optionally toggle **Set Qty All Items** to overwrite the **Quantity**
     on every copied detail line, then click the wizard's own **Confirm** button
     (`action_confirm` on the `copy_quotation_term` wizard — not the quotation's header
     **Confirm** button from `04-confirm`).
   - The **Items** table below is a read-only summary aggregated automatically from all
     payment term detail lines; it is not filled directly.
5. On the **Fix Item** tab, while the quotation is still in **Draft**, click **Recompute
   Price** to refresh `price_unit` on every product line from the current pricelist.
   This step is optional and may be skipped if the prices entered manually are already
   correct.
6. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The document number shows **/** until it is assigned when the quotation reaches the
  **In Progress** status.
