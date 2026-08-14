# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class ServiceContractFixItem(models.Model):
    """
    Extends Service Contract Fix Item with operating unit propagation.

    Stamps the Performance Obligation created by ``action_create_pob``
    (defined in ``ssi_service_revenue_recognition``) with the same
    ``operating_unit_id`` as the source contract (``service_id``), so
    it does not silently fall back to
    ``mixin.single_operating_unit``'s own default (the acting user's
    operating unit). See ``_prepare_pob_data`` below.
    """

    _name = "service.contract_fix_item"
    _inherit = [
        "service.contract_fix_item",
    ]

    def _prepare_pob_data(self):
        """Add the source contract's operating unit to the PoB data.

        Extends ``ssi_service_revenue_recognition``'s
        ``_prepare_pob_data`` so the Performance Obligation created by
        ``action_create_pob`` carries the same ``operating_unit_id``
        as this fix item's own service contract (``service_id``),
        instead of falling back to the acting user's default
        operating unit.

        :return: dict of values used to create the Performance
            Obligation, with ``operating_unit_id`` added
        """
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
