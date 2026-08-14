# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class ServiceContract(models.Model):
    """Attach quality control worksheets to ``service.contract``.

    Inherits ``mixin.qc_worksheet`` and enables its auto-injected form
    page (``_qc_worksheet_create_page = True``), giving each service
    contract a ``Quality Control`` tab where worksheets can be
    generated from a worksheet set and their aggregated result
    tracked. See the ``mixin.qc_worksheet`` docstring for the fields
    and actions it contributes.
    """

    _name = "service.contract"
    _inherit = [
        "service.contract",
        "mixin.qc_worksheet",
    ]
    _qc_worksheet_create_page = True
