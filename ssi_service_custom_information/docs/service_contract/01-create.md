# Create Service Contract

> **Module:** ssi_service_custom_information\
> **Extends:** ssi_service — model `service.contract`, aksi `01-create`\
> **Inline Actions:** `action_reload_custom_info_template` (Template),
> `action_reload_custom_info` (Custom Info)

## Additional Fields

When this module is installed, the create form gains a **Custom Information** page:

- **Template**: The `custom_info.template` used to render this contract's custom
  properties. Automatically filled once **Type** is selected — the module wires an
  onchange that looks up the template configured for that **Type**. Clears back to empty
  if **Type** is cleared. The user may still change it manually afterward.
- **Custom Properties** (`custom_info_ids`): Grid of custom property values rendered
  from the selected **Template**. Optional; only meaningful once a **Template** is set.

The page also carries two buttons, provided by the underlying `mixin.custom_info`
(shipped with `ssi_custom_information_mixin`) rather than by this module's own field
definitions:

- **Template**: Re-runs the template lookup for the current **Type**, refilling
  **Template** the same way the onchange does. Use it if **Template** was cleared or
  changed manually and needs to be reset to the **Type**'s configured value.
- **Custom Info**: Regenerates the **Custom Properties** rows from the currently
  selected **Template**. Manual edits already made to existing rows are discarded when
  this is used.

Neither button is restricted to the Draft status.
