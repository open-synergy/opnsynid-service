odoo.define("ssi_service_quotation_work_log.service_quotation_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Delta-only tour (arketipe E1): this module only adds a Work
    // Log tab to service.quotation's create form. Menu navigation
    // and the base create/save flow are covered by
    // ssi_service_quotation's own tour
    // (ssi_service_quotation_service_quotation_create); this tour
    // stops right after asserting the tab is displayed.
    //
    // IK: docs/service_quotation/01-create.md
    tour.register(
        "ssi_service_quotation_work_log_service_quotation_create",
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
                content: "Work Log tab is displayed",
                trigger: ".o_notebook .nav-link:contains(Work Log)",
                run: function () {
                    // Assertion only. Delta stops here: this
                    // module does not change the rest of the
                    // create Flow.
                },
            },
        ]
    );
});
