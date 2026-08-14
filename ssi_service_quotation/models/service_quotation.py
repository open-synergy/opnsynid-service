# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class ServiceQuotation(models.Model):
    """Service quotation transactional document.

    Combines ``service.mixin`` (base state machine, fields shared with
    ``service.contract``) with ``mixin.transaction_win_lost`` for the
    ``win``/``lost`` outcome states. Marking a quotation as win creates
    a linked ``service.contract`` (:meth:`_create_contract`); cancelling
    it releases that link (:meth:`_cancel_contract`).
    """

    _name = "service.quotation"
    _inherit = [
        "service.mixin",
        "mixin.transaction_win_lost",
    ]
    _description = "Service Quotation"

    _statusbar_visible_label = "draft,confirm,open,win"

    _policy_field_order = [
        "confirm_ok",
        "open_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "win_ok",
        "lost_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]

    _header_button_order = [
        "action_confirm",
        "action_open",
        "action_approve_approval",
        "action_reject_approval",
        "action_win",
        "%(ssi_transaction_win_lost_mixin.base_select_lost_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_win",
        "dom_lost",
        "dom_cancel",
    ]

    fix_item_ids = fields.One2many(
        comodel_name="service.quotation_fix_item",
    )
    fix_item_payment_term_ids = fields.One2many(
        comodel_name="service.quotation_fix_item_payment_term",
    )
    contract_id = fields.Many2one(
        string="# Contract",
        comodel_name="service.contract",
        readonly=True,
        copy=False,
        ondelete="set null",
    )

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("win", "Win"),
            ("lost", "Lost"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        default="draft",
        copy=False,
    )

    @api.model
    def _get_policy_field(self):
        res = super(ServiceQuotation, self)._get_policy_field()
        policy_field = [
            "open_ok",
            "confirm_ok",
            "approve_ok",
            "win_ok",
            "lost_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    # Boilerplate — satu-satunya method yang boleh tanpa docstring
    # bersama _get_policy_field (lihat 10-docstring.md)
    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    def action_win(self):
        """Mark the quotation as won and create its linked contract.

        :return: None.
        """
        _super = super(ServiceQuotation, self)

        _super.action_win()

        for record in self.sudo():
            record._create_contract()

    def action_cancel(self, cancel_reason):
        """Cancel the quotation and release its linked contract, if any.

        :param cancel_reason: ``base.cancel_reason`` record.
        :return: None.
        """
        _super = super(ServiceQuotation, self)

        _super.action_cancel(cancel_reason=cancel_reason)

        for record in self.sudo():
            record._cancel_contract()

    def _cancel_contract(self):
        """Cancel and unlink this quotation's ``contract_id``, if set.

        :return: True if there was no linked contract to cancel; None
            otherwise (the field is cleared via :meth:`write`).
        """
        self.ensure_one()

        if not self.contract_id:
            return True

        contract = self.contract_id
        contract.action_cancel(cancel_reason=self.cancel_reason_id)
        self.write(self._prepare_cancel_contract())

    def _prepare_cancel_contract(self):
        """Build the ``write`` values that release the linked contract.

        :return: dict, always ``{"contract_id": False}``.
        """
        self.ensure_one()
        return {
            "contract_id": False,
        }

    def _create_contract(self):
        """Create a ``service.contract`` from this quotation and link it.

        :return: None, writes the new contract's id to ``contract_id``.
        """
        self.ensure_one()
        obj_contract = self.env["service.contract"]
        data = self._prepare_contract_data()
        temp_record = obj_contract.new(data)
        temp_record = self._compute_contract_onchange(temp_record)
        values = temp_record._convert_to_write(temp_record._cache)
        contract = obj_contract.create(values)
        self.write(
            {
                "contract_id": contract.id,
            }
        )

    def _compute_contract_onchange(self, temp_record):
        """Run the contract's default-filling onchanges on a new record.

        :param temp_record: ``service.contract`` in-memory record built
            with :meth:`~odoo.models.Model.new`.
        :return: the same ``temp_record``, with its journal/account/
            analytic group onchange defaults applied.
        """
        temp_record.onchange_fix_item_receivable_journal_id()
        temp_record.onchange_fix_item_receivable_account_id()
        temp_record.onchange_analytic_group_id()
        return temp_record

    def _prepare_contract_data(self):
        """Build the ``create`` values for the linked contract.

        :return: dict of values matching ``service.contract`` fields.
        """
        self.ensure_one()
        fix_item_payment_term_ids = []
        for payment_term in self.fix_item_payment_term_ids:
            data = payment_term._prepare_contract_data()
            fix_item_payment_term_ids.append((0, 0, data))
        return {
            "title": self.title,
            "partner_id": self.partner_id.id,
            "contact_partner_id": self.contact_partner_id
            and self.contact_partner_id.id
            or False,
            "type_id": self.type_id.id,
            "contractor_id": self.contractor_id and self.contractor_id.id or False,
            "contact_contractor_id": self.contact_contractor_id
            and self.contact_contractor_id.id
            or False,
            "user_id": self.user_id.id,
            "manager_id": self.manager_id.id,
            "company_id": self.company_id.id,
            "pricelist_id": self.pricelist_id.id,
            "currency_id": self.currency_id.id,
            "date": fields.Date.today(),
            "date_start": self.date_start,
            "date_end": self.date_end,
            "quotation_id": self.id,
            "fix_item_payment_term_ids": fix_item_payment_term_ids,
            "salesperson_id": self.salesperson_id.id,
            "sale_team_id": self.sale_team_id and self.sale_team_id.id or False,
        }

    def action_recompute_price(self):
        """Recompute ``price_unit`` on every draft quotation's lines.

        :return: None.
        """
        for rec in self.sudo().filtered(lambda s: s.state == "draft"):
            for term_id in rec.fix_item_payment_term_ids:
                for detail_id in term_id.detail_ids:
                    detail_id.onchange_price_unit()
