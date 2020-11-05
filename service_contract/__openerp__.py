# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Service Contract",
    "version": "8.0.1.0.1",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_cancel_reason",
        "base_terminate_reason",
        "base_print_policy",
        "base_multiple_approval",
        "account_accountant",
        "web_readonly_bypass",
        "base_ir_filters_active",
        "base_action_rule",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_groups_data.xml",
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/base_terminate_reason_configurator_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "data/product_pricelist_type_data.xml",
        "menu.xml",
        "views/service_contract_type_views.xml",
        "views/service_contract_views.xml",
    ],
    "installable": True,
}
