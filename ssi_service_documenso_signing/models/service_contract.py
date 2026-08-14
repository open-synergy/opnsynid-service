# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class ServiceContract(models.Model):
    """Add Documenso signature-based approval to ``service.contract``.

    Mixes in ``mixin.documenso_signing_approval`` so that, when the
    contract's approval template points to a Documenso signing
    template, confirming the contract creates a signature request
    instead of the usual approval records. The contract is approved
    once that request is signed, and rejected if it is cancelled.
    """

    _name = "service.contract"
    _inherit = [
        "service.contract",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
