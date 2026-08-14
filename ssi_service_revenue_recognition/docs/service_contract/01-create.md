# Create Service Contract

> **Module:** ssi_service_revenue_recognition\
> **Extends:** ssi_service — model `service.contract`, aksi `01-create`

## Additional Fields

On the **Analytic & Project** tab, this module adds two fields:

- **PoB Analytic Group**: Optional. The analytic group used when Performance Obligations
  are auto-created from this contract's fix items. Defaults from the selected **Type**'s
  own PoB Analytic Group whenever **Type** changes, but may be changed afterwards.
- **Analytic Budget**: Optional. The analytic budget this contract's Performance
  Obligations are tracked against. Editable unless the budget is locked — see **Lock
  Budget** in `02-edit`.

## Related Views

- A **Performance Obligations** tab is added to the form, showing **Total** and
  **Diff.** (this contract's own untaxed amount versus the total amount of Performance
  Obligations already created from it, both read-only) and the list of those Performance
  Obligations. Clicking **PoB(s)** opens the full list in its own view. This tab has
  nothing to fill in and is not a Flow step.
- A **PoB Cost/Rev** smart button (`action_open_pob_cost_revenue`) is added to the
  button box. It opens the analytic lines posted to this contract's Performance
  Obligations' own analytic accounts. Navigation only; nothing is written.
