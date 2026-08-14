/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_service_state_change_constrain.service_contract_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/service_contract/01-create.md (E1 delta — Additional
    // Fields + Inline Actions: action_reload_status_check_template,
    // action_reload_status_check)
    tour.register(
        "ssi_service_state_change_constrain_service_contract_field_status_check",
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
            // delta of ssi_service_state_change_constrain) — the
            // Status Checks tab added by mixin.status_check. Open it
            // first: the tab is not the active one by default
            // (patterns.md § notebook tabs).
            {
                content: "Open the Status Checks tab",
                trigger: ".o_notebook .nav-link:contains(Status Checks)",
            },

            // Delta-only tour: assert the Status Check Template field
            // and both reload buttons are present, then stop. It does
            // not fill any field and does not continue to Save (E1
            // delta-only; see odoo-development-ui-test
            // scope-and-boundaries.md).
            {
                content: "Status Check Template field is displayed",
                trigger: ".o_field_widget[name='status_check_template_id']",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Status Check Template button is displayed",
                trigger: "button[name='action_reload_status_check_template']:enabled",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "Status Check Item button is displayed",
                trigger: "button[name='action_reload_status_check']:enabled",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ]
    );
});
