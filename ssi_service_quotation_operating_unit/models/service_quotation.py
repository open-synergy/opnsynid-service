# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ServiceQuotation(models.Model):
    _name = "service.quotation"
    _inherit = [
        "service.quotation",
        "mixin.single_operating_unit",
    ]

    def _prepare_contract_data(self):
        self.ensure_one()
        _super = super(ServiceQuotation, self)
        result = _super._prepare_contract_data()
        result.update(
            {
                "operating_unit_id": self.operating_unit_id
                and self.operating_unit_id.id
                or False,
            }
        )
        return result
