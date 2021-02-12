# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Service Contract - Man Hour",
    "version": "8.0.1.0.0",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "hr_timesheet",
        "service_contract",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/service_contract_type_views.xml",
        "views/service_contract_views.xml",
        "views/service_contract_man_hour_views.xml",
    ],
    "installable": True,
}
