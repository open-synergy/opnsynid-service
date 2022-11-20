# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ServiceQuotation(models.Model):
    _name = "service.quotation"
    _inherit = [
        "service.quotation",
    ]

    def _compute_contract_onchange(self, temp_record):
        _super = super(ServiceQuotation, self)
        _super._compute_contract_onchange(temp_record)
        temp_record.onchange_auto_create_project()
        return temp_record
