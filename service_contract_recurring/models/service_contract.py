# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil import relativedelta
from openerp import api, fields, models


class ServiceContract(models.Model):
    _name = "service.contract"
    _inherit = "service.contract"

    recurring_item_receivable_journal_id = fields.Many2one(
        string="Recurring Item Receivable Journal",
        comodel_name="account.journal",
    )
    recurring_item_receivable_account_id = fields.Many2one(
        string="Recurring Item Receivable Account",
        comodel_name="account.account",
    )
    recurring_item_allowed_product_ids = fields.Many2many(
        string="Recurring Item Allowed Products",
        comodel_name="product.product",
        related="type_id.recurring_item_allowed_product_ids",
    )
    recurring_item_allowed_product_categ_ids = fields.Many2many(
        string="Recurring Item Allowed Product Categories",
        comodel_name="product.category",
        related="type_id.recurring_item_allowed_product_categ_ids",
    )
    recurring_item_ids = fields.One2many(
        string="Recurring Item",
        comodel_name="service.contract_recurring_item",
        inverse_name="contract_id",
        readonly=False,
    )
    recurring_service_ok = fields.Boolean(
        string="Recurring Service?",
        default=False,
    )
    recurring_period_ids = fields.One2many(
        string="Recurring Period",
        comodel_name="service.contract_recurring_period",
        inverse_name="contract_id",
        readonly=True,
    )
    recurring_period = fields.Integer(
        string="Recurring Service Period",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    recurring_period_lenght = fields.Selection(
        string="Recurring Service Period Lenght",
        selection=[
            ("month", "Monthly"),
        ],
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    recurring_period_num = fields.Integer(
        string="Recurring Service Period Number",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    def action_approve(self):
        _super = super(ServiceContract, self)
        _super.action_approve()
        for record in self:
            record.action_create_recurring_period()

    @api.multi
    def action_restart(self):
        _super = super(ServiceContract, self)
        _super.action_restart()
        for record in self:
            record._delete_recurring_period()

    @api.multi
    def action_create_recurring_period(self):
        for record in self:
            record._create_recurring_period()

    @api.multi
    def _delete_recurring_period(self):
        self.ensure_one()
        for period in self.recurring_period_ids:
            aa = period.analytic_account_id
            period.write({"analytic_account_id": False})
            aa.unlink()
        self.recurring_period_ids.unlink()

    @api.multi
    def _create_recurring_period(self):
        self.ensure_one()

        obj_recurring_period = self.env["service.contract_recurring_period"]
        date_start = self.date_start
        for _period_num in range(1, self.recurring_period_num + 1):
            date_end = self._get_recurring_period_date_end(date_start)
            data = {
                "contract_id": self.id,
                "date_start": date_start,
                "date_end": date_end,
            }
            period = obj_recurring_period.create(data)
            period._create_analytic_account()
            date_start = self._get_recurring_period_date_start(date_end)

    @api.multi
    def _get_recurring_period_date_end(self, date_start):
        self.ensure_one()

        dt_start = fields.Date.from_string(date_start)
        date_end = dt_start + relativedelta.relativedelta(
            months=self.recurring_period, days=-1
        )
        return fields.Date.to_string(date_end)

    @api.multi
    def _get_recurring_period_date_start(self, date_end):
        self.ensure_one()

        dt_end = fields.Date.from_string(date_end)
        date_start = dt_end + relativedelta.relativedelta(days=1)
        return fields.Date.to_string(date_start)
