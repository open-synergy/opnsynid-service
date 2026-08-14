# Mark Service Quotation as Win

> **Module:** ssi_service_quotation_risk_analysis\
> **Extends:** ssi_service_quotation — model `service.quotation`, aksi `07-win`

## Additional Post-Condition

- The **Service Contract** automatically created when the quotation is marked **Win**
  (see the base `07-win.md` Post-Condition) also carries over the quotation's selected
  **Risk Analysis**, so the new contract's own Risk Analysis tab is pre-filled with the
  same `risk_analysis` record.
