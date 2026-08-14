# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class ServiceType(models.Model):
    """
    Adds the auto project creation default to the service type.
    The value configured here is copied onto a new service contract's
    ``auto_create_project`` field via onchange when **Type** is
    selected.
    """

    _name = "service.type"
    _inherit = [
        "service.type",
    ]

    auto_create_project = fields.Boolean(
        string="Auto Create Project",
    )
