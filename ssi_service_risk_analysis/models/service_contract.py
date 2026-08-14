# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class ServiceContract(models.Model):
    """Attach a risk analysis link to ``service.contract``.

    Inherits ``mixin.risk_analysis`` and enables its auto-injected form
    page (``_risk_analysis_create_page = True``), giving each service
    contract a **Risk Analysis** tab where ``risk_analysis_id`` can be
    selected. ``_risk_analysis_partner_field_name`` points the mixin at
    ``partner_id`` so the field's selection domain
    (``allowed_risk_analysis_ids``) is restricted to risk analyses of
    the contract's own partner. See the ``mixin.risk_analysis``
    docstring for the fields it contributes.
    """

    _name = "service.contract"
    _inherit = [
        "service.contract",
        "mixin.risk_analysis",
    ]
    _risk_analysis_create_page = True
    _risk_analysis_partner_field_name = "partner_id"
