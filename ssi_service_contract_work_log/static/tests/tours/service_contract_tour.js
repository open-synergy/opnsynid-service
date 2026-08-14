odoo.define("ssi_service_contract_work_log.service_contract_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/service_contract/01-create.md (delta — extends ssi_service)
    //
    // Delta-only tour (arketipe E1): navigation is the same "open Service >
    // Contracts, click Create" flow already covered by ssi_service's own
    // create tour. The only thing this tour proves is that installing this
    // module adds a visible Work Log tab to the form — it does not save the
    // record or continue into confirm/approve, which stay ssi_service's
    // responsibility.
    tour.register(
        "ssi_service_contract_work_log_service_contract_create",
        {
            test: true,
            url: "/web",
        },
        [
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
            {
                content: "Additional Work Log tab is displayed",
                trigger: ".o_notebook .nav-link:contains(Work Log)",
                run: function () {
                    // Assertion only — the delta stops here. Saving and
                    // moving the contract through confirm/approve is
                    // ssi_service's own create tour, not this module's.
                },
            },
        ]
    );
});
