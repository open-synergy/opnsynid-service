# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class ServiceContractFixItemPaymentTerm(models.Model):
    _name = "service.contract_fix_item_payment_term"
    _inherit = "service.contract_fix_item_payment_term"

    @api.multi
    def _get_fix_item_receivable_journal(self):
        _super = super(ServiceContractFixItemPaymentTerm, self)
        result = _super._get_fix_item_receivable_journal()
        contract = self.contract_id
        if contract.operating_unit_id:
            obj_setting = self.env["service.contract_type_operating_unit"]
            criteria = [
                ("type_id", "=", contract.type_id.id),
                ("operating_unit_id", "=", contract.operating_unit_id.id)
            ]
            setting = obj_setting.search(criteria)
            if len(setting) > 0 and setting[0].fix_item_receivable_journal_id:
                result = setting[0].fix_item_receivable_journal_id
        return result

    @api.multi
    def _get_fix_item_receivable_account(self):
        _super = super(ServiceContractFixItemPaymentTerm, self)
        result = _super._get_fix_item_receivable_account()
        contract = self.contract_id
        if contract.operating_unit_id:
            obj_setting = self.env["service.contract_type_operating_unit"]
            criteria = [
                ("type_id", "=", contract.type_id.id),
                ("operating_unit_id", "=", contract.operating_unit_id.id)
            ]
            setting = obj_setting.search(criteria)
            if len(setting) > 0 and setting[0].fix_item_receivable_account_id:
                result = setting[0].fix_item_receivable_account_id
        return result
