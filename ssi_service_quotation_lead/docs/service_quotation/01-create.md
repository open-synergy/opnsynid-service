# Create Service Quotation

> **Module:** ssi_service_quotation_lead\
> **Extends:** ssi_service_quotation — model `service.quotation`, aksi `01-create`

## Additional Fields

- **# Lead**: Optional. The `crm.lead` this quotation originates from. Editable only
  while the quotation is in **Draft**; becomes read-only once the quotation leaves
  Draft. Choices are domain-filtered to leads whose partner shares the same commercial
  partner as the quotation's **Partner** — the field stays empty (no choices) until
  **Partner** is set.
