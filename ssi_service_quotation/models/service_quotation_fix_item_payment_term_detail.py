# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ServiceQuotationFixItemPaymentTermDetail(models.Model):
    """One product line of a service quotation payment term.

    Child of ``service.quotation_fix_item_payment_term``
    (``detail_ids``). :meth:`_prepare_contract_data` converts this line
    into the ``create`` values for the matching
    ``service.contract_fix_item_payment_term_detail`` line when the
    quotation is won.
    """

    _name = "service.quotation_fix_item_payment_term_detail"
    _description = "Service Fix Item Payment Term Detail"
    _inherit = [
        "service.fix_item_payment_term_detail_mixin",
    ]

    term_id = fields.Many2one(
        string="Service Payment Term",
        comodel_name="service.quotation_fix_item_payment_term",
        ondelete="cascade",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="term_id.service_id.pricelist_id",
        store=True,
    )

    @api.onchange(
        "currency_id",
    )
    def onchange_pricelist_id(self):
        """Placeholder onchange kept for pricelist-related overrides.

        :return: None. Deliberately empty: ``pricelist_id`` is a
            ``related`` field, so there is nothing to recompute here;
            the hook exists as an extension point for modules that add
            pricelist-driven pricing.
        """

    def _prepare_contract_data(self):
        """Build the ``(0, 0, {...})`` tuple data for the contract line.

        :return: dict of values matching
            ``service.contract_fix_item_payment_term_detail`` fields.
        """
        self.ensure_one()
        return {
            "name": self.name,
            "product_id": self.product_id.id and self.product_id.id or False,
            "account_id": self.account_id.id,
            "analytic_account_id": self.analytic_account_id
            and self.analytic_account_id.id
            or False,
            "price_unit": self.price_unit,
            "uom_quantity": self.uom_quantity,
            "uom_id": self.uom_id.id,
            "tax_ids": [(6, 0, self.tax_ids.ids)],
            "pricelist_id": self.pricelist_id.id,
            "currency_id": self.currency_id.id,
            "sequence": self.sequence,
        }
