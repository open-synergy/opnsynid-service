/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_service_quotation_risk_analysis_lead.service_quotation_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/service_quotation/01-create.md (E2a delta — Modified
        // Flow: # Lead auto-fills Risk Analysis). The onchange result
        // itself is unit-test territory (odoo-development-unit-test); this
        // tour only proves the create form reaches the point where both
        // delta fields — # Lead (ssi_service_quotation_lead) and Risk
        // Analysis (ssi_service_quotation_risk_analysis) — are present
        // together, which is the precondition for the onchange to fire.
        tour.register(
            "ssi_service_quotation_risk_analysis_lead_service_quotation_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Base Flow 1 — Open the Service > Quotations menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Service app",
                    trigger: '.o_app[data-menu-xmlid="ssi_service.menu_root_service"]',
                },
                {
                    content: "Open the Quotations menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_service_quotation.menu_service_quotation"]',
                },
                {
                    // Gate: wait for the Quotations action to actually be
                    // mounted, not just any list view left over from the
                    // landing action (patterns.md §A).
                    content: "Quotations list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Quotations)",
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

                // Modified Flow (docs/service_quotation/01-create.md, delta
                // of ssi_service_quotation_lead) — the # Lead field added
                // right after Contact's Contractor.
                {
                    content: "The # Lead field is present",
                    trigger: ".o_field_many2one[name='lead_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },

                // Modified Flow (docs/service_quotation/01-create.md, delta
                // of ssi_service_quotation_risk_analysis) — the Risk
                // Analysis tab is not the active one by default (patterns.md
                // § notebook tabs); open it first.
                {
                    content: "Open the Risk Analysis tab",
                    trigger: ".o_notebook .nav-link:contains(Risk Analysis)",
                },

                // Both delta fields are reachable together: this is the
                // precondition for onchange_risk_analysis_id (this module's
                // only addition) to fire when # Lead / Partner change.
                // Delta-only tour: it does not select a Lead, does not
                // assert the auto-filled value, and does not continue to
                // Save — value assertions of the onchange result are
                // odoo-development-unit-test territory.
                {
                    content: "Risk Analysis field is displayed",
                    trigger: ".o_field_widget[name='risk_analysis_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        );
    }
);
