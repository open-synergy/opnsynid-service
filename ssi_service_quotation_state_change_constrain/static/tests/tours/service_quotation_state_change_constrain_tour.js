// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_service_quotation_state_change_constrain." +
        "service_quotation_state_change_constrain_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/service_quotation/01-create.md (E1 delta -- Additional
        // Fields). Navigation (open menu -> New) is taken from the base IK
        // ssi_service_quotation/docs/service_quotation/01-create.md Flow
        // steps 1-2 -- see skill odoo-development-ui-test,
        // scope-and-boundaries.md §1 ("Backing dua file: tour extension =
        // base IK ∪ delta IK"). The delta assertion comes from this
        // module's own IK: the Status Checks tab is present on the create
        // form. The tour stops there; it does not fill, save, or confirm
        // (E1 delta-only).
        tour.register(
            "ssi_service_quotation_state_change_constrain_" +
                "service_quotation_create",
            {
                test: true,
                url: "/web",
            },
            [
                // ── Base Flow 1 — Open the Service > Quotations menu.
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

                // ── Base Flow 2 — Click the New button. (14.0: "Create")
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

                // ── Delta assertion — the Status Checks tab added by this
                // module is present on the create form. The tour stops
                // here (E1 delta-only).
                {
                    content: "The Status Checks tab is present",
                    trigger:
                        ".o_form_view.o_form_editable .o_notebook " +
                        ".nav-link:contains('Status Checks')",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);
