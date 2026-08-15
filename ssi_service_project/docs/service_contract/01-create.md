# Create Service Contract

> **Module:** ssi_service_project\
> **Extends:** ssi_service — model `service.contract`, aksi `01-create`

## Additional Fields

When this module is installed, the create form gains a new **Project** group (after
**Analytic & Project**) with two fields:

- **Auto Create Project**: Optional. Automatically filled from **Type**. Change if
  needed. When checked and **Project** is left empty, a `project.project` record is
  automatically created once the contract reaches **In Progress** — see `05-approve.md`.
- **Project**: Optional. Links the contract to an existing `project.project` record.
  When set, that project is refreshed (instead of a new one being created) once the
  contract reaches **In Progress**.
