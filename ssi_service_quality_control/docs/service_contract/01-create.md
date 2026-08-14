# Create Service Contract

> **Module:** ssi_service_quality_control\
> **Extends:** ssi_service — model `service.contract`, aksi `01-create`\
> **Inline Actions:** `action_create_qc_worksheet` (Create Worksheet From Set)

## Additional Fields

When this module is installed, the create form gains a **Quality Control** tab:

- **Worksheet Set**: Optional. Selects a `qc_worksheet_set` record — the set of
  worksheet types that **Create Worksheet From Set** (see below) generates for this
  contract.
- **Result Computation Method**: Required. Selection of **Automatic** or **Manual**,
  defaulting to **Automatic**. Determines whether **Final** (below) is derived from the
  generated worksheets or entered by hand.
- **Automatic**: Read-only, computed. `True` only when every worksheet listed in **QC
  Worksheets** is in state _Done_ and has passed. Only meaningful when **Result
  Computation Method** is **Automatic**.
- **Manual**: A plain checkbox, editable at any time regardless of **Result Computation
  Method**. Used as the value of **Final** when **Result Computation Method** is
  **Manual**.
- **Final**: Read-only, computed. Mirrors **Automatic** or **Manual**, whichever
  **Result Computation Method** selects.
- **QC Worksheets**: Read-only summary list of the worksheets generated for this
  contract. Opening a row navigates to that worksheet's own record — filling out a
  worksheet's questions is done there, not on this form.

## Modified Flow

- Anchor: on the base Flow, before step 5 (**Save**), a **Quality Control** tab is
  available on the form (alongside **Accounting** and **Analytic & Project**).
- On the **Quality Control** tab, click **Create Worksheet From Set** to generate one
  worksheet per type configured in **Worksheet Set**. It does nothing if **Worksheet
  Set** is empty, and does nothing if **QC Worksheets** already has rows — it does not
  regenerate or duplicate worksheets that already exist.

## Related Views

- **Open QC Worksheet**: Opens the list of worksheets already generated for this
  contract, filtered to this record. Navigation only — it does not write any field and
  is not part of preparing the contract itself.
