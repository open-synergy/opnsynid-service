# Create Service Quotation

> **Module:** ssi_service_quotation_work_log\
> **Extends:** ssi_service_quotation — model `service.quotation`, aksi `01-create`

## Additional Fields

When this module is installed, the create form gains a **Work Log** tab:

- **Work Log Analytic Account**: The analytic account used as the reference for work
  logs recorded against this quotation. Optional.
- **Estimation** (Work Estimation): The estimated number of work hours for this
  quotation. Optional; used to compute the **Remaining** and **Excess** figures once
  work logs are recorded.
- **Work Logs**: A list of `hr.work_log` entries. Click **Add a line** to record work
  directly on the quotation. Repeat as many times as needed.

## Additional Post-Condition

- The **Work Log** tab shows **Total**, **Remaining**, and **Excess** figures computed
  automatically from the **Estimation** and the recorded **Work Logs**. These are
  read-only and not filled directly.
