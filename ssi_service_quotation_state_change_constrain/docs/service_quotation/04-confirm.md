# Confirm Service Quotation

> **Module:** ssi_service_quotation_state_change_constrain\
> **Extends:** ssi_service_quotation — model `service.quotation`, aksi `04-confirm`

## Modified Validation

- When a **State Change Constraint** template is configured with a detail line targeting
  state `confirm`, Confirm will fail with an error naming the first unmet item if any of
  that line's required **Status Check** items (see `01-create`) is not yet passed (or
  bypassed). Which template applies, and which status check items it requires for
  `confirm`, is configuration-driven — not fixed by this module.
