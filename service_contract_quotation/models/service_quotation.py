# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ServiceQuotation(models.Model):
    _name = "service.quotation"
    _description = "Service Quotation"
    _inherit = [
        "service.common",
        "custom.info.mixin",
    ]
    _state_from = ["draft", "confirm"]

    @api.depends(
        "type_id",
        "company_id",
    )
    @api.multi
    def _compute_policy(self):
        _super = super(ServiceQuotation, self)
        _super._compute_policy()

    @api.depends(
        "fix_item_payment_term_ids",
        "fix_item_payment_term_ids.amount_untaxed",
        "fix_item_payment_term_ids.amount_tax",
        "fix_item_payment_term_ids.amount_total",
    )
    @api.multi
    def _compute_fix_item_total(self):
        _super = super(ServiceQuotation, self)
        _super._compute_fix_item_total()

    contract_id = fields.Many2one(
        string="# Contract",
        comodel_name="service.contract",
        readonly=True,
        copy=False,
        ondelete="set null",
    )
    fix_item_payment_term_ids = fields.One2many(
        comodel_name="service.quotation_fix_item_payment_term",
    )
    fix_item_ids = fields.One2many(
        comodel_name="service.quotation_fix_item",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "In Progress"),
            ("won", "Won"),
            ("lost", "Lost"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )
    won_date = fields.Datetime(
        string="Won Date",
        readonly=True,
        copy=False,
    )
    won_user_id = fields.Many2one(
        string="Won By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    lost_date = fields.Datetime(
        string="Lost Date",
        readonly=True,
        copy=False,
    )
    lost_user_id = fields.Many2one(
        string="Lost By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    won_ok = fields.Boolean(
        string="Can Mark as Won",
        compute="_compute_policy",
    )
    lost_ok = fields.Boolean(
        string="Can Mark as Lost",
        compute="_compute_policy",
    )
    is_req_start_date = fields.Boolean(
        comodel_name="service.contract_type",
        related="type_id.is_req_start_date",
        store=False,
    )
    is_req_end_date = fields.Boolean(
        comodel_name="service.contract_type",
        related="type_id.is_req_end_date",
        store=False,
    )
    start_date = fields.Date(
        string="Start Date",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    end_date = fields.Date(
        string="End Date",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    def action_won(self):
        for record in self:
            record.write(record._prepare_won_data())

    @api.multi
    def action_lost(self):
        for record in self:
            record.write(record._prepare_lost_data())

    @api.multi
    def _prepare_cancel_data(self):
        _super = super(ServiceQuotation, self)
        result = _super._prepare_cancel_data()
        contract = self.contract_id
        result.update(
            {
                "contract_id": False,
            }
        )
        if contract:
            contract.action_cancel()
        return result

    @api.multi
    def _prepare_won_data(self):
        self.ensure_one()
        contract = self._create_contract()
        return {
            "state": "won",
            "won_date": fields.Datetime.now(),
            "won_user_id": self.env.user.id,
            "contract_id": contract.id,
        }

    @api.multi
    def _prepare_lost_data(self):
        self.ensure_one()
        return {
            "state": "lost",
            "won_date": fields.Datetime.now(),
            "won_user_id": self.env.user.id,
        }

    @api.onchange(
        "type_id",
    )
    def onchange_custom_info_template_id(self):
        self.custom_info_template_id = False
        if self.type_id:
            self.custom_info_template_id = (
                self.type_id.quotation_custom_info_template_id
            )

    @api.multi
    def _create_contract(self):
        self.ensure_one()
        obj_contract = self.env["service.contract"]
        data = self._prepare_contract_data()
        temp_record = obj_contract.new(data)
        temp_record = self._compute_contract_onchange(temp_record)
        values = temp_record._convert_to_write(temp_record._cache)
        return obj_contract.create(values)

    @api.multi
    def _compute_contract_onchange(self, temp_record):
        temp_record.onchange_fix_item_receivable_journal_id()
        temp_record.onchange_fix_item_receivable_account_id()
        temp_record.onchange_parent_analytic_account_id()
        temp_record.onchange_custom_info_template_id()
        return temp_record

    @api.multi
    def _prepare_contract_data(self):
        self.ensure_one()
        fix_item_payment_term_ids = []
        date_start = self.start_date or fields.Date.today()
        date_end = self.end_date or False
        for payment_term in self.fix_item_payment_term_ids:
            data = payment_term._prepare_contract_data()
            fix_item_payment_term_ids.append((0, 0, data))
        return {
            "title": self.title,
            "partner_id": self.partner_id.id,
            "type_id": self.type_id.id,
            "responsible_id": self.responsible_id.id,
            "company_id": self.company_id.id,
            "pricelist_id": self.pricelist_id.id,
            "currency_id": self.currency_id.id,
            "date": fields.Date.today(),
            "date_start": date_start,
            "date_end": date_end,
            "quotation_id": self.id,
            "salesman_id": self.responsible_id.id,
            "fix_item_payment_term_ids": fix_item_payment_term_ids,
        }
