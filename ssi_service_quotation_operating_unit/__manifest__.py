# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Service Quotation + Operating Unit",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_service_quotation",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_group/service_quotation.xml",
        "security/ir_rule/service_quotation.xml",
        "views/service_quotation_views.xml",
    ],
    "demo": [],
}
