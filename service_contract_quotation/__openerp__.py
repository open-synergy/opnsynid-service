# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Service Contract Quotation",
    "version": "8.0.1.3.1",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "service_contract",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_groups_data.xml",
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "views/service_contract_type_views.xml",
        "views/service_quotation_views.xml",
        "views/service_contract_views.xml",
        "data/tile_tile_data.xml",
    ],
    "installable": True,
}
