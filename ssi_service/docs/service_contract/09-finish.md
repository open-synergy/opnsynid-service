# Finish Service Contract

> **Module:** ssi_service\
> **Model:** `service.contract`\
> **Menu:** Service > Contracts\
> **Actor:** user in group `Service Contract - User`\
> **State:** `open` → `done`\
> **Requires:** `05-approve`\
> **Inline Actions:** `action_create_invoice` (Create Invoice), `action_delete_invoice`
> (Delete Invoice), `action_disconnect_invoice` (Disconnect Invoice),
> `action_mark_as_manual` (Mark as Manual), `action_unmark_as_manual` (Unmark as
> Manual), `%(link_invoice_to_payment_term_action)d` (Link Invoice)

## Pre-Condition

- **Record:** Status is **In Progress** (`open`).
- **Config:** The `policy.template` grants `done_ok` to the actor.
- **Access:** User is in group `Service Contract - User`.

## Flow

1. Open the **Service > Contracts** menu.
2. Open the record to finish.
3. On the **Contract Items** tab, under **Payment Terms**, each line shows an invoicing
   status (**Uninvoiced**, **Invoiced**, or **Manually Controlled**). Manage invoicing
   for each line as needed before finishing the contract:
   - On an **Uninvoiced** line, click **Create Invoice** to generate a new customer
     invoice from that line's Details, and link it automatically. There is no other way
     to generate the invoice from this screen. Skipping this leaves the line without an
     invoice.
   - On an **Uninvoiced** line, click **Link Invoice** instead to attach an
     already-posted invoice of the same partner rather than creating a new one. In the
     wizard that appears, select the invoice from **# Invoice**, then click the wizard's
     own **Confirm** button (`action_confirm` on the `link_invoice_to_payment_term`
     wizard — not the contract's header **Confirm** button from `04-confirm`).
   - On an **Uninvoiced** line, click **Mark as Manual** to flag the line as manually
     controlled when it is (or will be) invoiced outside this contract; on a **Manually
     Controlled** line, click **Unmark as Manual** to revert it back to **Uninvoiced**.
   - On an **Invoiced** line, click **Delete Invoice** to unlink and delete the invoice,
     or click **Disconnect Invoice** to unlink it while keeping the invoice document
     itself.
4. Click the **Done** button.
5. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
