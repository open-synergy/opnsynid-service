# Mark Service Quotation as Win

> **Module:** ssi_service_quotation_custom_information\
> **Extends:** ssi_service_quotation — model `service.quotation`, aksi `07-win`

## Additional Post-Condition

- The **Custom Properties** values filled in on the quotation's **Custom Information**
  tab are copied to the same properties on the newly created **Service Contract**,
  matched by property. This happens automatically as part of clicking **Win**; there is
  no extra step in the Flow.
