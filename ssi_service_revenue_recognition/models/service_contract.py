# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class ServiceContract(models.Model):
    """Add Performance Obligation revenue recognition to service contract.

    Links a contract's analytic account to the Performance Obligations
    (PoB) generated from its fix items, tracks the total PoB amount
    against the contract's own untaxed amount, and lets the budget be
    locked once it should no longer be recomputed from fix items.
    """

    _name = "service.contract"
    _inherit = ["service.contract"]

    pob_analytic_group_id = fields.Many2one(
        string="PoB Analytic Group",
        comodel_name="account.analytic.group",
    )
    analytic_budget_id = fields.Many2one(
        string="# Analytic Budget",
        comodel_name="analytic_budget.budget",
    )
    lock_budget = fields.Boolean(
        string="Lock Budget",
        default=False,
        readonly=True,
    )
    pob_ids = fields.Many2many(
        string="Performance Obligations",
        comodel_name="performance_obligation",
        compute="_compute_pob_ids",
    )
    amount_total_pob = fields.Monetary(
        string="Total Performance Obligation",
        currency_field="currency_id",
        related="analytic_account_id.amount_total_pob",
        store=True,
    )
    amount_diff_pob = fields.Monetary(
        string="Performance Obligation Diff",
        currency_field="currency_id",
        compute="_compute_amount_diff_pob",
        store=True,
    )
    pob_cost_revenue_count = fields.Integer(
        string="# PoB Cost/Revenue",
        related="analytic_account_id.pob_cost_revenue_count",
    )

    @api.depends("analytic_account_id")
    def _compute_pob_ids(self):
        """Resolve the Performance Obligations sourced from this contract.

        Searches ``performance_obligation`` by
        ``source_analytic_account_id`` since a PoB does not itself point
        back to the contract that generated it.
        """
        PoB = self.env["performance_obligation"]
        for record in self:
            if record.analytic_account_id:
                record.pob_ids = PoB.search(
                    [("source_analytic_account_id", "=", record.analytic_account_id.id)]
                )
            else:
                record.pob_ids = PoB

    @api.depends(
        "analytic_account_id.amount_total_pob",
        "amount_untaxed",
    )
    def _compute_amount_diff_pob(self):
        """Compare the contract's untaxed amount against total PoB amount.

        A positive result means the contract's fix items have not yet
        been fully turned into Performance Obligations.
        """
        for record in self:
            record.amount_diff_pob = (
                record.amount_untaxed - record.analytic_account_id.amount_total_pob
            )

    @api.onchange("analytic_account_id")
    def onchange_analytic_budget_id(self):
        self.analytic_budget_id = False

    @api.onchange("type_id")
    def onchange_pob_analytic_group_id(self):
        self.pob_analytic_group_id = False
        if self.type_id:
            self.pob_analytic_group_id = self.type_id.pob_analytic_group_id

    @api.onchange("pob_analytic_group_id")
    def onchange_pob_analytic_group_propagate(self):
        if self.analytic_account_id and self.pob_analytic_group_id:
            self.analytic_account_id.group_id = self.pob_analytic_group_id

    def action_lock_budget(self):
        """Lock the contract's budget so it stops being recomputed."""
        for record in self.sudo():
            record._lock_budget()

    def action_unlock_budget(self):
        """Unlock the contract's budget so it can be recomputed again."""
        for record in self.sudo():
            record._unlock_budget()

    def _lock_budget(self):
        """Set ``lock_budget`` to ``True`` on this single contract."""
        self.ensure_one()
        self.write({"lock_budget": True})

    def _unlock_budget(self):
        """Set ``lock_budget`` to ``False`` on this single contract."""
        self.ensure_one()
        self.write({"lock_budget": False})

    def action_open_pob(self):
        """Open Performance Obligations sourced from this contract.

        :return: ``ir.actions.act_window`` dict on ``performance_obligation``
        """
        self.ensure_one()
        result = {
            "name": "Performance Obligations",
            "type": "ir.actions.act_window",
            "res_model": "performance_obligation",
            "view_mode": "tree,form",
            "domain": [
                ("source_analytic_account_id", "=", self.analytic_account_id.id)
            ],
        }
        return result

    def action_open_pob_cost_revenue(self):
        """Open analytic lines from this contract's PoBs' own accounts.

        Delegates to the contract's own analytic account, which owns
        the aggregation logic (a contract's AA is just one possible
        source of PoBs among several document types).
        """
        self.ensure_one()
        return self.analytic_account_id.action_open_pob_cost_revenue()

    @ssi_decorator.post_open_action()
    def _10_assign_source_analytic_to_pob(self):
        """Fill source_analytic_account_id on PoB created before AA was set."""
        self.ensure_one()
        if self.analytic_account_id:
            self.pob_ids.filtered(lambda p: not p.source_analytic_account_id).write(
                {"source_analytic_account_id": self.analytic_account_id.id}
            )

    @ssi_decorator.post_confirm_action()
    def _10_update_pob_analytic_group(self):
        """Propagate pob_analytic_group to analytic account on confirm."""
        self.ensure_one()
        if self.analytic_account_id and self.pob_analytic_group_id:
            self.analytic_account_id.group_id = self.pob_analytic_group_id
