# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class ServiceType(models.Model):
    """Add the Auto Create Project on PoB default to service type.

    The value configured here becomes the ``auto_create_project``
    default written onto a Performance Obligation created from one of
    this type's contracts' fix items — see
    ``service.contract_fix_item._prepare_pob_data``.
    """

    _name = "service.type"
    _inherit = [
        "service.type",
    ]

    pob_auto_create_project = fields.Boolean(
        string="Auto Create Project on PoB",
        default=False,
    )
