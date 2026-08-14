/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_service_custom_information.service_contract_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/service_contract/01-create.md (E1 delta — Additional
    // Fields: the Custom Information page, its Template/Custom
    // Properties fields, and the Template/Custom Info reload
    // buttons). The onchange result and the reload buttons' write
    // effects are unit-test territory (odoo-development-unit-test);
    // this tour only proves the create form reaches the page and
    // that every delta element is actually rendered there.
    tour.register(
        "ssi_service_custom_information_service_contract_create",
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

            // Modified Flow (docs/service_contract/01-create.md,
            // delta of ssi_service_custom_information) — open the
            // Custom Information page added by this module.
            {
                content: "Open the Custom Information tab",
                trigger: ".o_notebook .nav-link:contains(Custom Information)",
            },

            // Additional Fields — Template.
            {
                content: "The Template field is present",
                trigger: ".o_field_many2one[name='custom_info_template_id']",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Additional Fields — Custom Properties grid.
            {
                content: "The Custom Properties grid is present",
                trigger: ".o_field_widget[name='custom_info_ids']",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },

            // Inline Actions — Template / Custom Info reload buttons,
            // injected by mixin.custom_info. Delta-only tour: it does
            // not click them (both write o2m/related data and are
            // odoo-development-unit-test territory), it only proves
            // both are rendered and clickable.
            {
                content: "The Template reload button is present",
                trigger: "button[name='action_reload_custom_info_template']:enabled",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
            {
                content: "The Custom Info reload button is present",
                trigger: "button[name='action_reload_custom_info']:enabled",
                run: function () {
                    // Assertion only; do not trigger the default click.
                },
            },
        ]
    );
});
