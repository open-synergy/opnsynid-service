/* Copyright 2026 OpenSynergy Indonesia
 * Copyright 2026 PT. Simetri Sinergi Indonesia
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define("ssi_service_revenue_recognition.service_contract_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

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

    // IK: docs/service_contract/01-create.md (E1 delta — Additional
    // Fields, on the Analytic & Project tab).
    tour.register(
        "ssi_service_revenue_recognition_service_contract_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openContractsMenuSteps(), [
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
                    // Assertion only.
                },
            },

            // The new fields live on the Analytic & Project tab, which is
            // NOT the default active tab (Contract Items is first) — it
            // must be opened before asserting field visibility, otherwise
            // the fields are in the DOM but not :visible and the trigger
            // times out.
            {
                content: "Open the Analytic & Project tab",
                trigger: ".o_notebook .nav-link:contains(Analytic & Project)",
            },

            // Additional Fields (docs/service_contract/01-create.md) —
            // delta-only tour: it stops here, it does not fill any field
            // and does not continue to Save.
            {
                content: "PoB Analytic Group field is displayed",
                trigger: ".o_field_widget[name='pob_analytic_group_id']",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Analytic Budget field is displayed",
                trigger: ".o_field_widget[name='analytic_budget_id']",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/service_contract/02-edit.md (E2a delta — Modified Flow +
    // Inline Actions on an existing, already-open contract).
    tour.register(
        "ssi_service_revenue_recognition_service_contract_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openContractsMenuSteps(), openRecordSteps("TOUR SC RR Edit"), [
            // Base Flow — Click Edit (14.0 opens existing records
            // readonly).
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

            // Modified Flow — Contract Items tab is the default
            // active tab, no tab click needed for the gear button.
            {
                content: "Click Create PoB on the fix item row",
                trigger:
                    ".o_field_widget[name='fix_item_ids'] " +
                    ".o_data_row:contains(TOUR RR Product) " +
                    "button[name='action_create_pob']",
            },
            {
                // Gate: Odoo 14 disables a type="object" button
                // synchronously on click and only re-enables it once
                // the full RPC + form reload cycle completes
                // (patterns.md §M/§P) — this cannot be true before
                // the click finishes its round trip, regardless of
                // whether a Performance Obligation was actually
                // created (no value is asserted here).
                content: "Create PoB finished",
                trigger:
                    ".o_field_widget[name='fix_item_ids'] " +
                    ".o_data_row:contains(TOUR RR Product) " +
                    "button[name='action_create_pob']:enabled",
                run: function () {
                    // Assertion only.
                },
            },

            // Modified Flow — Lock/Unlock Budget live on the
            // Analytic & Project tab, which is NOT the default
            // active tab.
            {
                content: "Open the Analytic & Project tab",
                trigger: ".o_notebook .nav-link:contains(Analytic & Project)",
            },
            {
                content: "Lock Budget button is displayed",
                trigger: ".o_form_view button[name='action_lock_budget']:enabled",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Click Lock Budget",
                trigger: ".o_form_view button[name='action_lock_budget']",
            },
            {
                // Gate: Unlock Budget only becomes visible once
                // lock_budget flips to True — it cannot be visible
                // before Lock Budget is clicked.
                content: "Unlock Budget button is now displayed",
                trigger: ".o_form_view button[name='action_unlock_budget']:enabled",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Lock Budget button is no longer displayed",
                trigger:
                    ".o_form_view:not(:has(button[name='action_lock_budget']:visible))",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );
});
