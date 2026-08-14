# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ServiceContract(models.Model):
    """
    Adds Operating Unit traceability to service contracts.
    Links each contract to the operating unit it belongs to, drives the
    OU-scoped record rule, and lets the fix item payment term (and its
    detail lines) propagate that operating unit to the invoices/invoice
    lines they generate.
    """

    _name = "service.contract"
    _inherit = [
        "service.contract",
        "mixin.single_operating_unit",
    ]
