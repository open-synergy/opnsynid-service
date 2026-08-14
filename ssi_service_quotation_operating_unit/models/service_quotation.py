# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ServiceQuotation(models.Model):
    """
    Adds Operating Unit traceability to service quotations.
    Links each quotation to the operating unit it belongs to, drives the
    OU-scoped record rule, and propagates that operating unit to the
    ``service.contract`` created from the quotation, instead of falling
    back to the acting user's own default operating unit.
    """

    _name = "service.quotation"
    _inherit = [
        "service.quotation",
        "mixin.single_operating_unit",
    ]

    def _prepare_contract_data(self):
        """Build the ``service.contract`` values, stamped with this OU.

        Extends the base ``_prepare_contract_data`` so the contract
        generated when the quotation is won carries the quotation's own
        ``operating_unit_id`` (Pola A propagation), rather than the OU
        default of the user who triggers the win action.

        :return: dict of ``service.contract`` values
        """
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
