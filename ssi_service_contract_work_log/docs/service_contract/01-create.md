# Create Service Contract

> **Module:** ssi_service_contract_work_log\
> **Extends:** ssi_service — model `service.contract`, aksi `01-create`

## Additional Fields

When this module is installed, the create form gains a **Work Log** tab:

- **Estimation**: Optional. The estimated amount of work planned for the contract.
- **Analytic Account** (labeled **Work Log Analytic Account**): Optional. The analytic
  account new work log entries for this contract default to.
- **Total**, **Remaining**, **Excess**: Read-only. Automatically computed from the
  contract's linked work logs (`hr.work_log`) and the **Estimation** above; not filled
  directly.
- **Work Logs**: Read-only summary list of `hr.work_log` records linked to this
  contract. Work logs are created from their own menu, not from this tab.
