// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_service_documenso_signing.service_contract_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/service_contract/05-approve.md (E2a delta -- Modified Flow)
    // Navigation (open menu -> open record -> click Approve -> confirm the
    // dialog) is retraced from the base IK
    // ssi_service/docs/service_contract/05-approve.md Flow steps 1-4 -- see
    // skill odoo-development-ui-test, scope-and-boundaries.md §3 ("Backing
    // dua file: tour extension = base IK ∪ delta IK"). The delta assertion,
    // inserted right before the base's Flow step 3, proves the additional
    // "Signature Requests" page is visible on the form. The approval
    // template used by this fixture has no Documenso signing template
    // configured (out of scope -- Ruang Lingkup excludes configuring the
    // Documenso connector), so the base Approve click still completes the
    // document normally; that final state assertion proves the action
    // still finishes end to end with the new page in place.
    tour.register(
        "ssi_service_documenso_signing_service_contract_approve",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Base Flow 1 — Open the Service > Contracts menu.
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
                    // Assertion only; do not trigger the default click.
                },
            },

            // ── Base Flow 2 — Open the record to approve.
            {
                content: "Open the record",
                trigger: ".o_data_row:contains(TOUR-DS-SC-APPROVE) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Delta anchor — before clicking Approve (base Flow step 3),
            // open the Signature Requests page this module adds and prove
            // it is rendered.
            {
                content: "Open the Signature Requests tab",
                trigger: ".o_notebook .nav-link:contains(Signature Requests)",
            },
            {
                // Anchored to the group label, not the (empty) many2one
                // field -- a readonly field without a value renders as a
                // zero-pixel element and never becomes a visible trigger
                // (odoo-development-ui-test skill, patterns.md §O).
                content:
                    "Signature Requests page shows the Approval Signing Request group",
                trigger: ".o_horizontal_separator:contains(Approval Signing Request)",
                run: function () {
                    // Assertion only.
                },
            },

            // ── Base Flow 3 — Click the Approve button.
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },

            // ── Base Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // ── Additional Post-Condition — the action still completes:
            // status jumps straight to In Progress, same as the base
            // Post-Condition.
            {
                content: "Status is In Progress",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ]
    );
});
