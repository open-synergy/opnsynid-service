# Mark Service Quotation as Win

> **Module:** ssi_service_quotation_project\
> **Extends:** ssi_service_quotation — model `service.quotation`, aksi `07-win`

## Additional Post-Condition

- The **Service Contract** automatically created by this action (see the base module's
  Post-Condition) has its **Auto Create Project** field pre-filled from the quotation's
  **Type**: when the **Type**'s **Auto Create Project** is checked, the new contract's
  **Auto Create Project** is checked too. This mirrors the same default a user would get
  by manually selecting **Type** on a new Service Contract form (see the
  `ssi_service_project` module's onchange on **Type**), which the base contract-creation
  flow would otherwise skip.
