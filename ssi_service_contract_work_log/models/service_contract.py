# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class ServiceContract(models.Model):
    """Add work log tracking to ``service.contract``.

    Activates ``mixin.work_object`` on the service contract so hours
    worked against the contract can be logged (``hr.work_log``) and
    reviewed on a dedicated Work Log tab, alongside the contract's own
    lifecycle managed by ``ssi_service``.
    """

    _name = "service.contract"
    _inherit = [
        "service.contract",
        "mixin.work_object",
    ]

    _work_log_create_page = True
