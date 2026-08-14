# Edit Service Contract

> **Module:** ssi_service_revenue_recognition\
> **Extends:** ssi_service — model `service.contract`, aksi `02-edit`\
> **Inline Actions:** `action_create_pob` (gear icon button on the Items table),
> `action_lock_budget` (Lock Budget), `action_unlock_budget` (Unlock Budget)

## Additional Fields

See `01-create` for **PoB Analytic Group** and **Analytic Budget** — both remain
editable while editing an existing contract, subject to the Lock Budget state described
below.

## Modified Flow

- Anchor: on the Flow base's step _Change any of the fields described in `01-create`_,
  on the **Contract Items** tab, the read-only **Items** summary table gains a gear-icon
  button on each row. Clicking it creates a Performance Obligation for that row's
  product/price if one does not already exist yet (the row's **# PoB** column stays
  empty until then). This button is not restricted to a particular contract status, but
  the Performance Obligation it creates is only correctly linked to this contract's own
  analytic account once that account exists — which happens when the contract reaches
  **In Progress** (see the base module's `05-approve.md`). Optional: creating
  Performance Obligations is not required to Save or to progress the contract's own
  status; skipping it just leaves the Performance Obligations tab without a
  corresponding entry for that item.
- Anchor: on the same Flow base step, on the **Analytic & Project** tab, once an
  **Analytic Budget** has been selected, click **Lock Budget** to prevent **Analytic
  Budget** from being changed further (the field becomes read-only). Click **Unlock
  Budget** to allow changing it again. Neither button is restricted to a particular
  contract status.
