# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class ServiceContractFixItem(models.Model):
    _name = "service.contract_fix_item"
    _inherit = [
        "service.contract_fix_item",
    ]

    def _prepare_pob_data(self):
        self.ensure_one()
        _super = super(ServiceContractFixItem, self)
        result = _super._prepare_pob_data()
        result.update(
            {
                "operating_unit_id": self.service_id.operating_unit_id.id
                if self.service_id.operating_unit_id
                else False,
            }
        )
        return result
