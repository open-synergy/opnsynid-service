odoo.define("ssi_service_quotation_lead.service_quotation_lead_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Delta tour for E1 (Additional Fields) — reuses the base "open menu"
    // Flow step 1 from ssi_service_quotation, since the delta IK does not
    // repeat it. See docs/service_quotation/01-create.md (delta) plus
    // ssi_service_quotation/docs/service_quotation/01-create.md (base).
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
                content: "Quotations list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Quotations)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; gate before touching the list.
                },
            },
        ];
    }

    // IK: docs/service_quotation/01-create.md (delta — Additional Fields)
    tour.register(
        "ssi_service_quotation_lead_service_quotation_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openQuotationsMenuSteps(), [
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
                content: "The additional # Lead field is present",
                trigger: ".o_field_many2one[name='lead_id']",
                run: function () {
                    // Assertion only — delta tour stops here, it does not
                    // fill in Partner/save/confirm (that is the base
                    // module's own 01-create tour).
                },
            },
        ])
    );
});
