odoo.define("ssi_service_quotation.service_quotation_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared "Flow step 1" for every service.quotation IK: open the
    // Service > Quotations menu and wait for the Quotations action to be
    // the one actually installed (not the app's landing action).
    function openQuotationsMenuSteps() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Service app",
                trigger: '.o_app[data-menu-xmlid="ssi_service.menu_root_service"]',
            },
            {
                content: "Open the Quotations menu",
                trigger:
                    ".o_menu_sections " +
                    '[data-menu-xmlid="ssi_service_quotation.menu_service_quotation"]',
            },
            {
                content: "Quotations list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Quotations)",
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
    // (e.g. ssi_service's service_contract_tour.js): bare
    // `.o_field_widget[name='x']`, no " input" suffix, run: "text ...".
    // InputField.init() (web/static/src/js/fields/basic_fields.js) sets
    // `this.tagName = 'input'` whenever `this.mode === 'edit'`, so
    // FieldChar's *root* element is already a literal <input> once the
    // field is genuinely in edit mode.
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

    // IK: docs/service_quotation/01-create.md
    tour.register(
        "ssi_service_quotation_service_quotation_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openQuotationsMenuSteps(), [
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
                "TOUR SQ Create",
                {extra_trigger: ".o_form_view.o_form_editable"}
            ),
            {
                content: "Select the Partner",
                trigger: ".o_field_many2one[name='partner_id'] input",
                run: "text TOUR Service Quotation Partner",
            },
            {
                content: "Pick the Partner from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(" +
                    "TOUR Service Quotation Partner)",
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
                run: "text TOUR Service Quotation Type",
            },
            {
                content: "Pick the Type from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(" +
                    "TOUR Service Quotation Type)",
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
                content: "Open the Fix Item tab",
                trigger: ".o_notebook .nav-link:contains(Fix Item)",
            },
            {
                content: "Add a Payment Term line",
                trigger:
                    ".o_field_widget[name='fix_item_payment_term_ids'] " +
                    ".o_field_x2many_list_row_add a",
            },
            {
                // The field carries both an inline <tree> AND an inline
                // <form>, so "Add a line" opens the line in a
                // FormViewDialog (a modal) instead of an inline editable
                // row. Do NOT prefix with `.modal` here: in_modal
                // defaults to true, so the trigger is already searched
                // INSIDE the modal.
                //
                // Gate on the "name" field's own rendered tag, not just
                // .o_form_editable on the outer container: InputField.
                // init() only sets `this.tagName = 'input'` once
                // `this.mode === 'edit'` for THAT WIDGET — the dialog's
                // outer form can already carry o_form_editable while an
                // individual field widget is still mid-render.
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
                // o_form_button_save. Multi-select mode (new record)
                // puts "Save & Close" first, so match its label.
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

    // IK: docs/service_quotation/02-edit.md
    tour.register(
        "ssi_service_quotation_service_quotation_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openQuotationsMenuSteps(), openRecordSteps("TOUR SQ Edit"), [
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
                run: "text TOUR SQ Edit - Updated",
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

    // IK: docs/service_quotation/03-delete.md
    tour.register(
        "ssi_service_quotation_service_quotation_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openQuotationsMenuSteps(), openRecordSteps("TOUR SQ Delete"), [
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

    // IK: docs/service_quotation/04-confirm.md
    tour.register(
        "ssi_service_quotation_service_quotation_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openQuotationsMenuSteps(), openRecordSteps("TOUR SQ Confirm"), [
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },
            confirmDialogStep(),
            statusIsStep("confirm", "Waiting for Approval"),
        ])
    );

    // IK: docs/service_quotation/05-approve.md
    tour.register(
        "ssi_service_quotation_service_quotation_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openQuotationsMenuSteps(), openRecordSteps("TOUR SQ Approve"), [
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },
            confirmDialogStep(),
            statusIsStep("open", "In Progress"),
        ])
    );

    // IK: docs/service_quotation/06-reject.md
    tour.register(
        "ssi_service_quotation_service_quotation_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(openQuotationsMenuSteps(), openRecordSteps("TOUR SQ Reject"), [
            {
                content: "Click the Reject button",
                trigger: ".o_statusbar_buttons button[name='action_reject_approval']",
                extra_trigger: ".o_form_view",
            },
            confirmDialogStep(),
            statusIsStep("reject", "Rejected"),
        ])
    );

    // IK: docs/service_quotation/07-win.md
    tour.register(
        "ssi_service_quotation_service_quotation_win",
        {
            test: true,
            url: "/web",
        },
        [].concat(openQuotationsMenuSteps(), openRecordSteps("TOUR SQ Win"), [
            {
                content: "Click the Win button",
                trigger: ".o_statusbar_buttons button[name='action_win']",
                extra_trigger: ".o_form_view",
            },
            confirmDialogStep(),
            statusIsStep("win", "Win"),
        ])
    );

    // IK: docs/service_quotation/08-lost.md
    tour.register(
        "ssi_service_quotation_service_quotation_lost",
        {
            test: true,
            url: "/web",
        },
        [].concat(openQuotationsMenuSteps(), openRecordSteps("TOUR SQ Lost"), [
            {
                content: "Click the Lost button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Lost')",
                extra_trigger: ".o_form_view",
            },
            {
                content: "The lost reason wizard is open",
                // 14.0: trigger is searched INSIDE the modal already
                // (in_modal defaults to true) — do not prefix `.modal`.
                trigger: ".o_field_radio[name='lost_reason_id']",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Select the Lost Reason",
                trigger: ".o_field_radio[name='lost_reason_id'] input:first",
            },
            {
                content: "Click Confirm on the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },
            confirmDialogStep(),
            statusIsStep("lost", "Lost"),
        ])
    );

    // IK: docs/service_quotation/09-cancel.md
    tour.register(
        "ssi_service_quotation_service_quotation_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openQuotationsMenuSteps(), openRecordSteps("TOUR SQ Cancel"), [
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                extra_trigger: ".o_form_view",
            },
            {
                content: "The cancellation wizard is open",
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

    // IK: docs/service_quotation/10-restart.md
    tour.register(
        "ssi_service_quotation_service_quotation_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(openQuotationsMenuSteps(), openRecordSteps("TOUR SQ Restart"), [
            {
                content: "Click the Restart button",
                trigger: ".o_statusbar_buttons button[name='action_restart']",
                extra_trigger: ".o_form_view",
            },
            confirmDialogStep(),
            statusIsStep("draft", "Draft"),
        ])
    );
});
