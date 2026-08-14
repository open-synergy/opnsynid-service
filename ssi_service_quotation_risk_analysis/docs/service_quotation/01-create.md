# Create Service Quotation

> **Module:** ssi_service_quotation_risk_analysis\
> **Extends:** ssi_service_quotation — model `service.quotation`, aksi `01-create`

## Additional Fields

When this module is installed, the create form gains a **Risk Analysis** tab:

- **Risk Analysis**: Optional. Selects a `risk_analysis` record for the quotation's
  **Partner**. The selection list is domain-filtered to non-cancelled risk analyses
  whose partner matches the quotation's **Partner** (commercial partner).
- **Risk Analysis State**: Read-only. Shows the status of the selected **Risk
  Analysis**; empty until one is selected.
- **Risk Analysis Result**: Read-only. Automatically filled from the selected **Risk
  Analysis** once that risk analysis reaches **Done**; empty otherwise. Not filled
  directly by the user.
