# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class ServiceQuotation(models.Model):
    """Attach a risk analysis link to ``service.quotation``.

    Inherits ``mixin.risk_analysis`` and enables its auto-injected form
    page (``_risk_analysis_create_page = True``), giving each service
    quotation a **Risk Analysis** tab where ``risk_analysis_id`` can be
    selected. ``_risk_analysis_partner_field_name`` points the mixin at
    ``partner_id`` so the field's selection domain
    (``allowed_risk_analysis_ids``) is restricted to risk analyses of
    the quotation's own partner. See the ``mixin.risk_analysis``
    docstring for the fields it contributes.
    """

    _name = "service.quotation"
    _inherit = [
        "service.quotation",
        "mixin.risk_analysis",
    ]
    _risk_analysis_create_page = True
    _risk_analysis_partner_field_name = "partner_id"

    def _prepare_contract_data(self):
        """Carry the selected risk analysis into the generated contract.

        Extends the base ``_prepare_contract_data`` values with
        ``risk_analysis_id`` so the ``service.contract`` created when
        this quotation is won keeps the same risk analysis link.

        :return: dict of ``service.contract`` values
        """
        self.ensure_one()
        _super = super(ServiceQuotation, self)
        result = _super._prepare_contract_data()
        result.update(
            {
                "risk_analysis_id": self.risk_analysis_id
                and self.risk_analysis_id.id
                or False,
            }
        )
        return result
