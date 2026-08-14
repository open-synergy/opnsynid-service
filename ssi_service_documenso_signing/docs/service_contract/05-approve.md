# Approve Service Contract

> **Module:** ssi_service_documenso_signing
>
> **Extends:** ssi_service — model `service.contract`, aksi `05-approve`

## Modified Flow

- Anchor: on Flow base step 3 (Click the **Approve** button). This module adds a
  **Signature Requests** page to the form (present from record creation onward, inserted
  after the last existing tab), showing the **Approval Signature Request** field
  (`approval_signature_request_id`) plus the record's full signing history.
- When the matching `approval.template` has a Documenso signing template configured,
  Confirm (base `04-confirm.md`) already created a single `documenso.signature.request`
  instead of a per-level approval record, and it is shown in that field. From this point
  in the base Flow, the manual Approve click described above does not apply to this
  document: there is no `approval.approval` record for the pending level, so there is
  nothing to click Approve on for it. Approval is granted automatically once the linked
  signature request reaches the **Signed** state in Documenso.
- If the signature request is cancelled instead (e.g. a signer declines in Documenso),
  this document moves straight to **Rejected** — the same outcome as clicking Reject in
  the base Flow (`06-reject.md`), but triggered by Documenso instead of by a user
  action.
- When the approval template has **no** Documenso signing template configured, the base
  Flow above applies unchanged; the **Signature Requests** page is still visible but its
  **Approval Signature Request** field stays empty.

## Additional Post-Condition

- Once the signature request reaches **Signed**, this document completes exactly as
  described in the base Post-Condition: since the approval template defines a single
  approver level, status changes directly to **In Progress** and the document number and
  analytic account are generated automatically as usual.
