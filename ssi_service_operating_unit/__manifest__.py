# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Service Contract + Operating Unit",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_service",
        "ssi_operating_unit_mixin",
        "ssi_financial_accounting_operating_unit",
    ],
    "data": [
        "security/res_group/service_contract.xml",
        "security/ir_rule/service_contract.xml",
        "views/service_contract_views.xml",
    ],
    "demo": [],
}
