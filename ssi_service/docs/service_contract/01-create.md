# Create Service Contract

> **Module:** ssi_service\
> **Model:** `service.contract`\
> **Menu:** Service > Contracts\
> **Actor:** user in group `Service Contract - User`\
> **State:** `—` → `draft`

## Pre-Condition

- **Config:** An active `policy.template` for `service.contract` is installed (shipped
  with the module).
- **Config:** An active `sequence.template` for `service.contract` is installed (shipped
  with the module).
- **Data:** A `service.type` record exists (see `service.type` master data).
- **Data:** A `res.partner` record exists to use as the contract's **Partner**.
- **Access:** User is in group `Service Contract - User`.

## Flow

1. Open the **Service > Contracts** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Title** _(required)_: Free-text title of the contract.
   - **Partner** _(required)_: The customer this contract is for.
   - **Contact**: Optional. Domain-filtered to contacts of the selected Partner.
   - **Sale Team**: Optional.
   - **Salesperson** _(required)_: Domain-filtered to allowed salespersons.
   - **Contractor**: Optional.
   - **Contact's Contact**: Optional. Domain-filtered to contacts of the selected
     Contractor.
   - **Type** _(required)_: The `service.type` that governs allowed products,
     pricelists, and the default receivable journal/account/analytic group.
   - **Manager** _(required)_: The user responsible for the contract.
   - **Date** _(required)_: Reference date used by the document sequence.
   - **Date Start** / **Date End** _(required)_: The contract's active period.
   - **Currency** _(required)_.
   - **Pricelist** _(required)_: Domain-filtered to pricelists allowed by **Type** and
     matching **Currency**.
   - **Fix Item Receivable Journal**, **Fix Item Receivable Account**, **Analytic
     Group** (on the **Accounting** and **Analytic & Project** tabs): Automatically
     filled from **Type**. Change if needed.
   - **Recipient Bank** (on the **Accounting** tab): Optional. Domain-filtered to the
     contract company's bank accounts.
4. On the **Contract Items** tab, under **Payment Terms**, click **Add a line** to add
   at least one payment term. Repeat as many times as needed:
   - **Term**: Name of the payment term line.
   - **Date Invoice Estimation**: Optional.
   - Under the term's **Details** sub-table, click **Add a line** to add each product
     line. Repeat as many times as needed:
     - **Product**: Domain-filtered to products/categories allowed by **Type**.
     - **Description**, **Usage**, **Account**, **Quantity**, **UoM**, **Price Unit**,
       **Taxes**.
   - The **Items** table below is a read-only summary aggregated automatically from all
     payment term detail lines; it is not filled directly.
5. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The document number shows **/** until it is assigned when the contract reaches the
  **Open** status.
