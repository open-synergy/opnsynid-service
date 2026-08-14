odoo.define("ssi_service.service_contract_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared "Flow step 1" for every service.contract IK: open the
    // Service > Contracts menu and wait for the Contracts action to be
    // the one actually installed (not the app's landing action).
    function openContractsMenuSteps() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Service app",
                trigger: '.o_app[data-menu-xmlid="ssi_service.menu_root_service"]',
            },
            {
                content: "Open the Contracts menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_service.menu_service_contract"]',
            },
            {
                content: "Contracts list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Contracts)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; gate before touching the list.
                },
            },
        ];
    }

    function openRecordSteps(title) {
        return [
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(" + title + ") .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
        ];
    }

    function confirmDialogStep() {
        return {
            content: "Confirm the dialog",
            trigger: ".modal-footer button.btn-primary",
            in_modal: true,
        };
    }

    function statusIsStep(value, label) {
        return {
            content: "Status is " + label,
            trigger:
                ".o_statusbar_status .o_arrow_button[data-value='" +
                value +
                "'].btn-primary",
            run: function () {
                // Assertion only.
            },
        };
    }

    // Fill a Char field the same way every other CI-passing SSI tour does
    // (e.g. ssi-loan's loan_type_tour.js, ssi-va's va_biller_tour.js):
    // bare `.o_field_widget[name='x']`, no " input" suffix, run: "text ...".
    // This works because InputField.init() (web/static/src/js/fields/
    // basic_fields.js) sets `this.tagName = 'input'` whenever
    // `this.mode === 'edit'`, so FieldChar's *root* element — the one
    // `_renderEdit()` hands to `_prepareInput()`, which becomes `this.$el`
    // AND `this.$input` — is already a literal <input> once the field is
    // genuinely in edit mode. There is no separate nested <input> to
    // select, and no need to hand-dispatch events: Tip.getConsumeEventType()
    // sees a real <input type="text">, returns "input", and
    // RunningTourActionHelper._text() takes its normal `.val(text)` +
    // native event branch.
    function fillCharField(content, trigger, value, extraStepProps) {
        return Object.assign(
            {
                content: content,
                trigger: trigger,
                run: "text " + value,
            },
            extraStepProps || {}
        );
    }

    // IK: docs/service_contract/01-create.md
    tour.register(
        "ssi_service_service_contract_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openContractsMenuSteps(), [
            {
                content: "Click Create",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only.
                },
            },
            fillCharField(
                "Fill in Title",
                ".o_field_widget[name='title']",
                "TOUR SC Create",
                {extra_trigger: ".o_form_view.o_form_editable"}
            ),
            {
                content: "Select the Partner",
                trigger: ".o_field_many2one[name='partner_id'] input",
                run: "text TOUR Service Partner",
            },
            {
                content: "Pick the Partner from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR Service Partner)",
                in_modal: false,
            },
            {
                content: "Select the Salesperson",
                trigger: ".o_field_many2one[name='salesperson_id'] input",
                run: "text Mitchell Admin",
            },
            {
                content: "Pick the Salesperson from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(Mitchell Admin)",
                in_modal: false,
            },
            {
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text TOUR Service Type",
            },
            {
                content: "Pick the Type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR Service Type)",
                in_modal: false,
            },
            {
                content: "Select the Manager",
                trigger: ".o_field_many2one[name='manager_id'] input",
                run: "text Mitchell Admin",
            },
            {
                content: "Pick the Manager from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(Mitchell Admin)",
                in_modal: false,
            },
            {
                content: "Fill in Date",
                trigger: ".o_field_widget[name='date'] input",
                run: "text 01/15/2026",
            },
            {
                content: "Fill in Date Start",
                trigger: ".o_field_widget[name='date_start'] input",
                run: "text 01/15/2026",
            },
            {
                content: "Fill in Date End",
                trigger: ".o_field_widget[name='date_end'] input",
                run: "text 12/15/2026",
            },
            {
                content: "Select the Currency",
                trigger: ".o_field_many2one[name='currency_id'] input",
                run: "text USD",
            },
            {
                content: "Pick USD from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(USD)",
                in_modal: false,
            },
            {
                content: "Select the Pricelist",
                trigger: ".o_field_many2one[name='pricelist_id'] input",
                run: "text Public Pricelist",
            },
            {
                content: "Pick the Pricelist from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(Public Pricelist)",
                in_modal: false,
            },
            {
                content: "Open the Contract Items tab",
                trigger: ".o_notebook .nav-link:contains(Contract Items)",
            },
            {
                content: "Add a Payment Term line",
                trigger:
                    ".o_field_widget[name='fix_item_payment_term_ids'] " +
                    ".o_field_x2many_list_row_add a",
            },
            {
                // The field carries both an inline <tree> AND an inline
                // <form>, so "Add a line" opens the line in a FormViewDialog
                // (a modal) instead of an inline editable row. Do NOT
                // prefix with `.modal` here: in_modal defaults to true, so
                // the trigger is already searched INSIDE the modal — a
                // `.modal` prefix would look for a modal nested in a modal.
                //
                // Gate on the "name" field's own rendered tag, not just
                // .o_form_editable on the outer container: InputField.init()
                // (web/static/src/js/fields/basic_fields.js) only sets
                // `this.tagName = 'input'` once `this.mode === 'edit'` for
                // THAT WIDGET, and _renderEdit() -> _prepareInput() is what
                // actually turns this.$el into the live this.$input. The
                // dialog's outer form can already carry o_form_editable
                // while an individual field widget is still mid-render (in
                // which case it's still a plain <span>, not <input>) —
                // gating on the container alone lets the next step race
                // that per-field render, leaving FieldChar._getValue()
                // reading .val() off an undefined this.$input.
                content: "The line dialog's Term name field is ready",
                trigger: "input.o_field_widget[name='name']",
                run: function () {
                    // Assertion only.
                },
            },
            fillCharField(
                "Fill in the Term name",
                ".o_field_widget[name='name']",
                "TOUR Term Create"
            ),
            {
                // FormViewDialog buttons carry only "btn-primary", never
                // o_form_button_save — see web/static/src/js/views/
                // view_dialogs.js FormViewDialog.init(). Multi-select mode
                // (new record) puts "Save & Close" first, so match its label.
                content: "Save & Close the line dialog",
                trigger: ".modal-footer button.btn-primary:contains('Save & Close')",
                in_modal: true,
            },
            {
                content: "The line was added",
                trigger:
                    ".o_field_widget[name='fix_item_payment_term_ids'] " +
                    ".o_data_row:contains(TOUR Term Create)",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },
            statusIsStep("draft", "Draft"),
        ])
    );

    // IK: docs/service_contract/02-edit.md
    tour.register(
        "ssi_service_service_contract_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openContractsMenuSteps(), openRecordSteps("TOUR SC Edit"), [
            {
                content: "Click the Edit button",
                trigger: ".o_form_button_edit",
            },
            {
                content: "Form is now editable",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Change the Title",
                trigger: ".o_field_widget[name='title']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR SC Edit - Updated",
            },
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/service_contract/03-delete.md
    tour.register(
        "ssi_service_service_contract_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openContractsMenuSteps(), openRecordSteps("TOUR SC Delete"), [
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Delete",
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Delete";
                        }
                    );
                    $delete[0].click();
                },
            },
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Back to the list",
                trigger: ".o_list_view",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/service_contract/04-confirm.md
    tour.register(
        "ssi_service_service_contract_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openContractsMenuSteps(), openRecordSteps("TOUR SC Confirm"), [
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },
            confirmDialogStep(),
            statusIsStep("confirm", "Waiting for Approval"),
        ])
    );

    // IK: docs/service_contract/05-approve.md
    tour.register(
        "ssi_service_service_contract_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openContractsMenuSteps(), openRecordSteps("TOUR SC Approve"), [
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },
            confirmDialogStep(),
            statusIsStep("open", "In Progress"),
        ])
    );

    // IK: docs/service_contract/06-reject.md
    tour.register(
        "ssi_service_service_contract_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(openContractsMenuSteps(), openRecordSteps("TOUR SC Reject"), [
            {
                content: "Click the Reject button",
                trigger: ".o_statusbar_buttons button[name='action_reject_approval']",
                extra_trigger: ".o_form_view",
            },
            confirmDialogStep(),
            statusIsStep("reject", "Rejected"),
        ])
    );

    // IK: docs/service_contract/09-finish.md
    tour.register(
        "ssi_service_service_contract_finish",
        {
            test: true,
            url: "/web",
        },
        [].concat(openContractsMenuSteps(), openRecordSteps("TOUR SC Finish"), [
            {
                content: "Open the Contract Items tab",
                trigger: ".o_notebook .nav-link:contains(Contract Items)",
            },
            {
                content: "Click Mark as Manual on the payment term line",
                trigger:
                    ".o_field_widget[name='fix_item_payment_term_ids'] " +
                    ".o_data_row:contains(TOUR Term Finish) " +
                    "button[name='action_mark_as_manual']",
            },
            {
                // Gate: this button only appears once the line's own
                // state moved from "uninvoiced" to "manual" — it
                // cannot be true before Mark as Manual is clicked.
                content: "The line is now Manually Controlled",
                trigger:
                    ".o_field_widget[name='fix_item_payment_term_ids'] " +
                    ".o_data_row:contains(TOUR Term Finish) " +
                    "button[name='action_unmark_as_manual']",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Click the Done button",
                trigger: ".o_statusbar_buttons button[name='action_done']",
                extra_trigger: ".o_form_view",
            },
            confirmDialogStep(),
            statusIsStep("done", "Done"),
        ])
    );

    // IK: docs/service_contract/10-cancel.md
    tour.register(
        "ssi_service_service_contract_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openContractsMenuSteps(), openRecordSteps("TOUR SC Cancel"), [
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                extra_trigger: ".o_form_view",
            },
            {
                content: "The cancellation wizard is open",
                // 14.0: trigger is searched INSIDE the modal already
                // (in_modal defaults to true) — do not prefix `.modal`.
                trigger: ".o_field_radio[name='cancel_reason_id']",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Select the Cancellation Reason",
                trigger: ".o_field_radio[name='cancel_reason_id'] input:first",
            },
            {
                content: "Click Confirm on the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },
            confirmDialogStep(),
            statusIsStep("cancel", "Cancelled"),
        ])
    );

    // IK: docs/service_contract/11-terminate.md
    tour.register(
        "ssi_service_service_contract_terminate",
        {
            test: true,
            url: "/web",
        },
        [].concat(openContractsMenuSteps(), openRecordSteps("TOUR SC Terminate"), [
            {
                content: "Click the Terminate button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Terminate')",
                extra_trigger: ".o_form_view",
            },
            {
                content: "The termination wizard is open",
                trigger: ".o_field_radio[name='terminate_reason_id']",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Select the Termination Reason",
                trigger: ".o_field_radio[name='terminate_reason_id'] input:first",
            },
            {
                content: "Click Confirm on the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },
            confirmDialogStep(),
            statusIsStep("terminate", "Terminated"),
        ])
    );

    // IK: docs/service_contract/12-restart.md
    tour.register(
        "ssi_service_service_contract_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(openContractsMenuSteps(), openRecordSteps("TOUR SC Restart"), [
            {
                content: "Click the Restart button",
                trigger: ".o_statusbar_buttons button[name='action_restart']",
                extra_trigger: ".o_form_view",
            },
            confirmDialogStep(),
            statusIsStep("draft", "Draft"),
        ])
    );

    // IK: docs/service_contract/13-reset-number.md
    tour.register(
        "ssi_service_service_contract_reset_number",
        {
            test: true,
            url: "/web",
        },
        [].concat(openContractsMenuSteps(), openRecordSteps("TOUR SC Reset"), [
            {
                content: "Click the Reset Document Number button",
                trigger:
                    ".o_statusbar_buttons " +
                    "button[name='action_reset_document_number']",
                extra_trigger: ".o_form_view",
            },
            confirmDialogStep(),
            {
                // Service.contract's name field is "/" again, but the h1
                // title shows display_name, not name directly — and
                // MixinTransaction.name_get() (ssi_transaction_mixin/
                // models/mixin_transaction.py) special-cases the "/"
                // value: when the document number field equals "/", the
                // displayed name becomes "*" + str(record.id), never the
                // literal "/" character. setUpClass gives this record a
                // non-"/" starting name (no leading "*"), so this gate
                // cannot be true before Reset Document Number runs.
                content: "Document number is back to /",
                trigger:
                    ".o_form_view .oe_title h1 " +
                    ".o_field_widget[name='display_name']:contains(*)",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );
});
