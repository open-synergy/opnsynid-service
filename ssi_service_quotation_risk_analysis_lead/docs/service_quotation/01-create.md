# Create Service Quotation

> **Module:** ssi_service_quotation_risk_analysis_lead\
> **Extends:** ssi_service_quotation — model `service.quotation`, aksi `01-create`

## Additional Pre-Condition

- **Module:** `ssi_service_quotation_risk_analysis` and `ssi_service_quotation_lead` are
  both installed (this module auto-installs once both are present).

## Modified Flow

- Anchor: base Flow step 3 (Fill in the required fields), after **# Lead** (added by
  `ssi_service_quotation_lead`) and **Risk Analysis** (added by
  `ssi_service_quotation_risk_analysis`) are filled in.
- Selecting a **# Lead**, or changing **Partner** while a **# Lead** is already
  selected, automatically fills **Risk Analysis** with that lead's own
  `risk_analysis_id`, if the lead has one set.
- Changing **Partner** while no **# Lead** is selected clears **Risk Analysis** back to
  empty.
- The auto-fill only sets an initial value — the user may still change **Risk Analysis**
  manually afterward.
