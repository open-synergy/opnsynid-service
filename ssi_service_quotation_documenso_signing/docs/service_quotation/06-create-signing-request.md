# Create Signing Request for Service Quotation

> **Module:** ssi_service_quotation_documenso_signing\
> **Model:** `service.quotation`\
> **Menu:** Service > Quotations\
> **Actor:** user in group `Service Quotation - User`\
> **Requires:** `ssi_service_quotation/service_quotation/01-create`\
> **Extends:** ssi_service_quotation — model `service.quotation`

## Pre-Condition

- **Record:** A `service.quotation` record exists. The **Signature Requests** tab is
  present on the form regardless of status, since
  `_documenso_signing_create_page = True` is set unconditionally by this module.
- **Config:** An active `documenso.signing.template` exists with **Source Model** set to
  `service.quotation` and a **Py3o Report** configured. The Py3o Report is required
  because the created `documenso.signature.request` copies it from the template and
  requires it to save; without one, clicking **Create** in step 6 fails.
- **Config:** An active `documenso.backend` exists.
- **Access:** User is in group `Service Quotation - User` — the button carries no
  additional group restriction beyond normal record access.

## Flow

1. Open the **Service > Quotations** menu.
2. Open the record.
3. Open the **Signature Requests** tab.
4. Click the **New Signing Request** button.
5. In the wizard that appears, fill in:
   - **Signing Template** _(required)_: select the Documenso Signing Template configured
     for **Service Quotation**.
   - **Backend**: Automatically filled with the active Documenso Backend. Change if
     needed.
6. Click **Create**. The browser navigates to the newly created signature request's own
   form.
7. Return to the **Service > Quotations** menu, open the same record again, and open the
   **Signature Requests** tab.

## Post-Condition

- A new row appears in the list on the **Signature Requests** tab, for the signature
  request just created. The row's field values are not asserted.
- This action does not move `service.quotation`'s own status.

## Note — Open Signature Requests button

- The **Open Signature Requests** button on the same **Signature Requests** tab
  (`action_open_signature_requests`) is verdict **N** (nol IK): it only returns an
  `ir.actions.act_window` that opens the list of this record's signature requests — it
  writes no field. No IK or tour is written for it.
