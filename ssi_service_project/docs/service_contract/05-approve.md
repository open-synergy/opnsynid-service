# Approve Service Contract

> **Module:** ssi_service_project **Extends:** ssi_service — model `service.contract`,
> aksi `05-approve`

## Additional Post-Condition

- When **Auto Create Project** is checked, a `project.project` record is automatically
  created and linked via **Project** once the contract reaches **In Progress** (`open`)
  — unless **Project** was already set, in which case that existing project is refreshed
  instead. This is not a Flow step; it runs automatically as part of the same Approve
  action documented in the base module's `05-approve.md`.
