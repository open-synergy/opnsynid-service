# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

from odoo import api, models


class ServiceQuotation(models.Model):
    """
    Adds status check and state change constraint to service quotations.

    Extends ``service.quotation`` with a **Status Checks** tab
    (``mixin.status_check``) and a state change gate
    (``mixin.state_change_constrain``) that, when a matching
    ``state.change.constrain.template`` is configured, blocks a state
    transition until every required status check item is satisfied.
    """

    _name = "service.quotation"
    _inherit = [
        "service.quotation",
        "mixin.state_change_constrain",
        "mixin.status_check",
    ]

    _status_check_create_page = True

    @api.onchange("type_id")
    def onchange_status_check_template_id(self):
        """Re-select the status check template when Type changes.

        Clears ``status_check_template_id`` first, then re-resolves it
        via ``_get_template_status_check`` (``mixin.status_check``) so
        the **Status Checks** tab always matches the record's current
        **Type**.
        """
        self.status_check_template_id = False
        if self.type_id:
            self.status_check_template_id = self._get_template_status_check()

    # @api.model_create_multi
    # def create(self, vals_list):
    #     _super = super(ServiceQuotation, self)
    #     quotation = _super.create(vals_list)
    #     quotation.action_reload_status_check_template()
    #     quotation.action_reload_status_check()
    #     return quotation
