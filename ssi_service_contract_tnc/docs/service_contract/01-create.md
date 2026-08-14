# Create Service Contract

> **Module:** ssi_service_contract_tnc\
> **Extends:** ssi_service — model `service.contract`, aksi `01-create`\
> **Inline Actions:** `action_generate_tnc` (Generate T&C)

## Additional Fields

When this module is installed, the create form gains a **Terms & Conditions** tab:

- **T&C Template**: Optional. Selects a `tnc_template` record configured for the
  `service.contract` model. Selecting a template does not by itself fill in the
  **Sections** / **Clauses** lists below — click **Generate T&C** (see below).
- **Sections**: A list of T&C sections attached to the contract. Rows may be added
  manually with **Add a line**, or generated in bulk from **T&C Template** with
  **Generate T&C**.
- **Clauses**: Read-only. Automatically aggregated from the clauses of every row in
  **Sections** — not filled directly by the user.

On the **Terms & Conditions** tab, click **Generate T&C** to (re)build **Sections**
(and, through it, **Clauses**) from the selected **T&C Template**. Running it again
after changing **T&C Template** first discards the sections generated previously, then
rebuilds them from the new template. If **T&C Template** is empty, **Generate T&C**
discards any existing sections and leaves the lists empty — it does not fail.
