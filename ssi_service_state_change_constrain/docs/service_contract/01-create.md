# Create Service Contract

> **Module:** ssi_service_state_change_constrain\
> **Extends:** ssi_service — model `service.contract`, aksi `01-create`\
> **Inline Actions:** `action_reload_status_check_template` (Status Check Template),
> `action_reload_status_check` (Status Check Item)

## Additional Fields

When this module is installed, the create form gains a **Status Checks** tab, visible
only to users in the **Settings / Technical** group (`base.group_system`):

- **Status Check Template**: The `status.check.template` used to build the checklist
  below. Automatically (re)selected whenever **Type** changes, based on the contract's
  data — it is not required to pick it manually.
- **Status Check** (list, read-only rows): One line per item defined by the selected
  **Status Check Template**. Each line carries a **Status Ok** checkbox the user ticks
  off as the corresponding condition is satisfied. This list is not filled by typing —
  it is built by the **Status Check Item** button (see below).

On the **Status Checks** tab, two buttons rebuild the checklist:

- **Status Check Template**: Re-runs the automatic template selection (the same logic as
  the **Type** onchange above) and writes the result to **Status Check Template**.
- **Status Check Item**: Regenerates the **Status Check** list from the currently
  selected **Status Check Template** — adding lines for items not yet present and
  removing lines whose item is no longer part of the template.

## Additional Post-Condition

- A **State Change Constrain Template** may be auto-selected on record creation
  (`state.change.constrain.template`, matched against the record's **Status Check
  Template**). This field is internal — it is not shown on any form — and only
  determines whether later state transitions are gated; see the **Modified Validation**
  note on `04-confirm` and `05-approve`.
