# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Service Contract Integration Operating Unit",
    "version": "8.0.1.2.0",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "service_contract",
        "analytic_operating_unit",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/service_contract_ir_rule_data.xml",
        "data/base_sequence_configurator_data.xml",
        "views/service_contract_views.xml",
        "views/service_contract_type_views.xml",
    ],
    "installable": True,
}
