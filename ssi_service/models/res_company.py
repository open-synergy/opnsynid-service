# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ResCompany(models.Model):
    """Extension point reserved for company-level service settings.

    Currently adds no fields; kept so future service configuration
    options have a place to land without introducing a new inherit.
    """

    _name = "res.company"
    _inherit = "res.company"
