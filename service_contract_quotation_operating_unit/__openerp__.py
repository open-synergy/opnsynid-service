# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Service Contract Quotation + Operating Unit",
    "version": "8.0.1.0.0",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "service_contract_operating_unit",
        "service_contract_quotation",
    ],
    "data": [
        "security/service_quotation_ir_rule_data.xml",
        "views/service_quotation_views.xml",
        "views/service_contract_type_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
