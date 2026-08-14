# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class ServiceContract(models.Model):
    """Attach Terms & Conditions to ``service.contract``.

    Inherits ``mixin.tnc`` and enables its auto-injected form page
    (``_tnc_create_page = True``), giving each service contract a
    ``T&C Template`` field plus generated sections/clauses. See the
    ``mixin.tnc`` docstring for the fields and the ``Generate T&C``
    action it contributes.
    """

    _name = "service.contract"
    _inherit = [
        "service.contract",
        "mixin.tnc",
    ]

    _tnc_create_page = True
