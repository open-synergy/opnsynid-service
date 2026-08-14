# Edit Service Contract

> **Module:** ssi_service_revenue_recognition_project\
> **Extends:** ssi_service_revenue_recognition — model `service.contract`, aksi `02-edit`

## Additional Post-Condition

- When the Inline Action `action_create_pob` (gear icon button on the Items table,
  documented in the base extension's `02-edit.md`) creates a Performance Obligation for
  a fix item line, the resulting `performance_obligation` record's own **Auto Create
  Project** field is defaulted from this contract's **Type**'s own **Auto Create Project
  on PoB** field — a new checkbox this module adds to the **Service Type** form. This is
  not a Flow step; it happens automatically as part of the same `action_create_pob`
  click. The Performance Obligation's **Auto Create Project** field and the project
  auto-creation itself are provided by module `ssi_revenue_recognition_project`, not
  part of this repository.
