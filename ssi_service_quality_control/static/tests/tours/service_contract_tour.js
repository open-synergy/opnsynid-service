/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_service_quality_control.service_contract_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/service_contract/01-create.md (E1 delta — Additional
    // Fields + Inline Actions: action_create_qc_worksheet)
    tour.register(
        "ssi_service_quality_control_service_contract_field_qc_worksheet",
        {
            test: true,
            url: "/web",
        },
        [
            // Base Flow 1 — Open the Service > Contracts menu.
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
                // Gate: wait for the Contracts action to actually be
                // mounted, not just any list view left over from the
                // landing action (patterns.md §A).
                content: "Contracts list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Contracts)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Base Flow 2 — Click the New button.
            {
                content: "Click New",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Additional Fields (docs/service_contract/01-create.md,
            // delta of ssi_service_quality_control) — the Quality
            // Control tab added by mixin.qc_worksheet. Open it first:
            // the tab is not the active one by default (patterns.md §
            // notebook tabs).
            {
                content: "Open the Quality Control tab",
                trigger: ".o_notebook .nav-link:contains(Quality Control)",
            },

            // Delta-only tour: assert the Worksheet Set field and the
            // Create Worksheet From Set button are present, then stop.
            // It does not fill any field and does not continue to Save
            // (E1 delta-only; see odoo-development-ui-test
            // scope-and-boundaries.md).
            {
                content: "Worksheet Set field is displayed",
                trigger: ".o_field_widget[name='qc_worksheet_set_id']",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Create Worksheet From Set button is displayed",
                trigger: "button[name='action_create_qc_worksheet']:enabled",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ]
    );
});
