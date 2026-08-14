# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, models


class ServiceQuotation(models.Model):
    """Wire the ``lead_id`` field to the ``risk_analysis_id`` field.

    This module adds no field of its own: ``lead_id`` comes from
    ``ssi_service_quotation_lead`` and ``risk_analysis_id`` comes from
    ``ssi_service_quotation_risk_analysis``. The only addition here is
    an onchange that carries the selected lead's own risk analysis
    over to the quotation, so the user does not have to pick the same
    risk analysis twice.
    """

    _name = "service.quotation"
    _inherit = [
        "service.quotation",
    ]

    @api.onchange(
        "lead_id",
        "partner_id",
    )
    def onchange_risk_analysis_id(self):
        self.risk_analysis_id = False
        if self.lead_id:
            self.risk_analysis_id = self.lead_id.risk_analysis_id
