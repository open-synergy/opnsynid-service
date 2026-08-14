# Create Service Quotation

> **Module:** ssi_service_quotation_state_change_constrain\
> **Extends:** ssi_service_quotation — model `service.quotation`, aksi `01-create`

## Additional Fields

When this module is installed, the create form gains a **Status Checks** tab:

- **Status Check Template**: Automatically (re)selected whenever **Type** changes — the
  first `status.check.template` configured for `service.quotation` whose condition
  evaluates true for the record. Visible only to users in the _Technical Settings_
  group; not user-editable through this field directly (use the **Status Check
  Template** button described below to force a re-selection).
- **Status Check** (list, read-only): The checklist items copied from the selected
  **Status Check Template**. Each item shows whether it currently passes. This list is
  what a later state change constraint (see `04-confirm` and `05-approve`) checks
  against.

The tab also carries two buttons, **Status Check Template** and **Status Check Item**
(both visible only to the _Technical Settings_ group), that force a re-evaluation of the
template and the checklist items respectively — normally not needed, since both are kept
in sync automatically on create and whenever **Type** changes.

## Additional Post-Condition

- The new record's **Status Checks** tab is already populated: `status_check_ids` is
  filled from the selected `status_check_template_id`, and — if a matching
  `state.change.constrain.template` is configured — `state_change_constrain_template_id`
  is auto-selected as well. Neither blocks Draft; they only take effect on the next
  state change (see `04-confirm` and `05-approve`).
