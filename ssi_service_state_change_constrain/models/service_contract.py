# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

from odoo import api, models


class ServiceContract(models.Model):
    """Add State Change Constrain + Status Check to ``service.contract``.

    :cvar _status_check_create_page: Show the "Status Checks" tab on the
        ``service.contract`` form (restricted to ``base.group_system``).
    :cvar _status_check_include_fields: Fields whose change re-evaluates
        the auto-selected Status Check Template via
        :meth:`onchange_status_check_template_id`.
    """

    _name = "service.contract"
    _inherit = [
        "service.contract",
        "mixin.state_change_constrain",
        "mixin.status_check",
    ]

    _status_check_create_page = True
    _status_check_include_fields = [
        "type_id",
        "partner_id",
    ]

    @api.onchange("type_id")
    def onchange_status_check_template_id(self):
        """Re-select the Status Check Template when ``type_id`` changes.

        Clears ``status_check_template_id`` first, then looks up the
        matching ``status.check.template`` for the current record via
        ``mixin.status_check._get_template_status_check()``. Left empty
        when ``type_id`` is not set.
        """
        self.status_check_template_id = False
        if self.type_id:
            self.status_check_template_id = self._get_template_status_check()

    # @api.model_create_multi
    # def create(self, vals_list):
    #     _super = super(ServiceContract, self)
    #     contract = _super.create(vals_list)
    #     contract.onchange_status_check_template_id()
    #     return contract
