# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class ServiceQuotation(models.Model):
    """Adds Documenso electronic signature support to service quotations.

    Extends ``service.quotation`` with
    ``mixin.documenso_signing_approval`` so the quotation approval flow
    can be driven by a Documenso signature request instead of manual
    approvers. Setting ``_documenso_signing_create_page`` to ``True``
    injects the Documenso signing tab into the quotation form view.
    """

    _name = "service.quotation"
    _inherit = [
        "service.quotation",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
