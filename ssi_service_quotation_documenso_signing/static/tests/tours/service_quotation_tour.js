// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_service_quotation_documenso_signing.service_quotation_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared "open the Service > Quotations menu" steps, matching the base
    // IK ssi_service_quotation/docs/service_quotation Flow step 1.
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
                // Gate: wait for the TARGET action to be mounted, not just
                // any list view (the app may land on a stale list first).
                content: "Quotations list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Quotations)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
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
                content: "Record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/service_quotation/05-approve.md (E2a delta -- Modified Flow)
    // Navigation (open menu -> open record) is retraced from the base IK
    // ssi_service_quotation/docs/service_quotation/05-approve.md Flow
    // steps 1-2 -- see skill odoo-development-ui-test,
    // scope-and-boundaries.md §3 ("E2a -- telusur-ulang aksi itu dari base
    // sampai titik ubah"). The delta assertion, anchored at base Flow step
    // 2 (open the record to approve), verifies the Signature Requests tab
    // injected because `_documenso_signing_create_page = True`, then stops
    // -- base Flow steps 3-4 (Approve / OK) and the resulting In Progress
    // status are NOT exercised here, since whether the Approve button is
    // even visible depends on whether the active Approval Template has a
    // Documenso Signing Template configured, and this tour's fixture
    // leaves that unconfigured. The final signed/rejected outcome is
    // driven by the external Documenso connector and out of scope for a
    // tour (Keputusan Desain, issue
    // open-synergy/opnsynid-service#113).
    tour.register(
        "ssi_service_quotation_documenso_signing_service_quotation_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openQuotationsMenuSteps(),
            openRecordSteps("Tour SQ Documenso Approve"),
            [
                // ── Delta assertion (anchor: base Flow step 2) — the
                // Signature Requests tab is always present once this
                // module is installed, regardless of whether Documenso
                // signing is actually used for the current approval.
                {
                    content: "Open the Signature Requests tab",
                    trigger: ".o_notebook .nav-link:contains(Signature Requests)",
                },
                {
                    // Anchored on the group label rather than the
                    // (currently empty) `approval_signature_request_id`
                    // many2one widget itself -- a many2one rendered with
                    // no value has no text node inside its link, so it
                    // collapses to a zero-size box and jQuery's
                    // `:visible` (offsetWidth/offsetHeight) never matches
                    // it, hanging the tour until timeout. The group
                    // label always has text, so it is a stable proxy for
                    // "the Approval Signing Request group is rendered".
                    content:
                        "Signature Requests tab shows the Approval Signing " +
                        "Request group",
                    trigger:
                        ".o_horizontal_separator:contains(Approval Signing Request)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action. The tour stops here -- it does not click
                        // Approve, does not assert a final state, and
                        // never calls the external Documenso service.
                    },
                },
            ]
        )
    );

    // IK: docs/service_quotation/06-create-signing-request.md (E3 -- new
    // action). The tour runs the wizard to completion (Create), which
    // navigates to the newly created documenso.signature.request's own
    // form -- it does NOT go further and click that request's own "Send
    // to Documenso" button, since that would call the external Documenso
    // service over the network. After the wizard, the tour returns to the
    // Service Quotation record and re-opens the Signature Requests tab to
    // observe the new row -- the row's field values are not asserted
    // (Keputusan Desain, issue open-synergy/opnsynid-service#113).
    tour.register(
        "ssi_service_quotation_documenso_signing_service_quotation" +
            "_create_signing_request",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openQuotationsMenuSteps(),
            openRecordSteps("Tour SQ Documenso Signing Request"),
            [
                // ── Flow 3 — Open the Signature Requests tab.
                {
                    content: "Open the Signature Requests tab",
                    trigger: ".o_notebook .nav-link:contains(Signature Requests)",
                },

                // ── Flow 4 — Click the New Signing Request button.
                {
                    content: "Click the New Signing Request button",
                    trigger:
                        ".o_form_view button[name='action_create_signing_request']",
                },

                // ── Flow 5 — In the wizard that appears, fill in Signing
                // Template (Backend is filled automatically).
                {
                    // 14.0: do not prefix the trigger with `.modal` -- the
                    // tour manager already searches inside the modal, and
                    // `.modal .o_form_view` would look for a nested modal
                    // that does not exist (patterns.md §H).
                    content: "The Create Signing Request wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default
                        // click action.
                    },
                },
                {
                    content: "Select the Signing Template",
                    trigger: ".o_field_many2one[name='signing_template_id'] input",
                    run: "text Tour SQ Documenso Signing Template",
                },
                {
                    content: "Pick the Signing Template from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(Tour SQ " +
                        "Documenso Signing Template)",
                    in_modal: false,
                },

                // ── Flow 6 — Click Create. The browser navigates to the
                // newly created signature request's own form.
                {
                    content: "Click Create",
                    trigger: ".modal-footer button[name='action_confirm']",
                },
                {
                    // The button's return action keeps the existing
                    // breadcrumb trail and appends the new record's OWN
                    // display_name (`name_get()` on
                    // documenso.signature.request, e.g. "*20 - Tour SQ
                    // Documenso Backend (draft)") -- it is NOT the static
                    // act_window "name" ("Signature Request"), and that
                    // display name is data-dependent (source record id +
                    // backend + state), so it is not a stable string to
                    // assert on. Anchor instead on the "Py3o Report"
                    // field, which only exists on
                    // documenso.signature.request's own form (never on
                    // the wizard or on service.quotation), and is filled
                    // with the fixture's report name -- a gate that
                    // cannot match anywhere earlier in this tour.
                    content: "The new Signature Request's own form is displayed",
                    trigger:
                        ".o_field_widget[name='py3o_report_id']:contains(Tour SQ " +
                        "Documenso Py3o Report)",
                    extra_trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default
                        // click action. The tour does NOT click "Send to
                        // Documenso" here -- that would call the
                        // external Documenso service.
                    },
                },

                // ── Flow 7 — Return to the Quotations menu, reopen the
                // same record, and open the Signature Requests tab again.
            ].concat(openQuotationsMenuSteps(), [
                {
                    content: "Reopen the record",
                    trigger:
                        ".o_data_row:contains(Tour SQ Documenso Signing " +
                        "Request) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Reopen the Signature Requests tab",
                    trigger: ".o_notebook .nav-link:contains(Signature Requests)",
                },

                // ── Post-Condition — a new row appears on the
                // Signature Requests page for the request just
                // created. Its field values are not asserted
                // (Keputusan Desain).
                {
                    content: "A new row appears on the Signature Requests page",
                    trigger:
                        ".o_field_widget[name='signature_request_ids'] " +
                        ".o_data_row",
                    run: function () {
                        // Assertion only; do not trigger the default
                        // click action.
                    },
                },
            ])
        )
    );
});
