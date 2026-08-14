# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class ServiceContractFixItem(models.Model):
    """Add the Type's auto-create-project default to PoB creation.

    Extends ``_prepare_pob_data`` so a Performance Obligation created
    from this fix item line carries the contract's own Type's
    ``pob_auto_create_project`` value, letting
    ``ssi_revenue_recognition_project`` decide whether to auto-create
    a project once that Performance Obligation is confirmed.
    """

    _name = "service.contract_fix_item"
    _inherit = [
        "service.contract_fix_item",
    ]

    def _prepare_pob_data(self):
        """Add ``auto_create_project`` on top of the base PoB values.

        :return: dict of ``performance_obligation`` values, extending
            the base ``_prepare_pob_data`` result with
            ``auto_create_project`` sourced from ``service_id.type_id``
        """
        self.ensure_one()
        _super = super(ServiceContractFixItem, self)
        result = _super._prepare_pob_data()
        result.update(
            {
                "auto_create_project": self.service_id.type_id.pob_auto_create_project,
            }
        )
        return result
