odoo.define(
    "ssi_service_quotation_custom_information.service_quotation_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/service_quotation/01-create.md (delta)
        //
        // Delta-only tour (arketipe E1): navigation is taken from the base
        // `ssi_service_quotation` create tour (open menu, click New), then
        // this module's own contribution — the Custom Information tab — is
        // asserted to be rendered. It does not continue to save/confirm;
        // that remains fully covered by the base tour.
        tour.register(
            "ssi_service_quotation_custom_information_service_quotation_create",
            {
                test: true,
                url: "/web",
            },
            [
                tour.stepUtils.showAppsMenuItem(),
                {
                    // ── Flow 1 — Open the Service > Quotations menu.
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
                    // ── Flow 2 — Click the New button.
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
                    // ── Additional Fields — Custom Information tab.
                    content: "Open the Custom Information tab",
                    trigger: ".o_notebook .nav-link:contains(Custom Information)",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    // Anchor on the field's own label, not on the (empty,
                    // readonly-looking) many2one widget itself — an unset
                    // Template value renders as a zero-width element and
                    // the trigger would never match it.
                    content: "Custom Information tab shows the Template field",
                    trigger: ".o_form_label:contains(Template)",
                    run: function () {
                        // Assertion only. Post-Condition: the additional
                        // Custom Information tab and its Template field
                        // are rendered on the create form.
                    },
                },
            ]
        );
    }
);
