# Create Service Quotation

> **Module:** ssi_service_quotation_custom_information\
> **Extends:** ssi_service_quotation — model `service.quotation`, aksi `01-create`

## Additional Fields

When this module is installed, the **Custom Information** tab is added to the form
(after the last existing tab):

- **Custom Information Template**: Automatically set when **Type** is filled in —
  resolved from the `custom.info.template` records that apply to `service.quotation`,
  evaluated in sequence order. Read-only; not picked manually by the user.
- **Custom Properties**: One row per property defined by the resolved **Custom
  Information Template**. Rows appear automatically once the template is set; the user
  fills in each row's **Value** as needed. Rows are removed automatically if the
  template no longer defines that property.
