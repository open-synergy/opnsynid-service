# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ServiceType(models.Model):
    """Add Performance Obligation defaults to service type.

    Configures the default analytic group used when a contract of
    this type creates its Performance Obligations, and which products
    or product categories should have their PoB auto-created.
    """

    _name = "service.type"
    _inherit = [
        "service.type",
    ]

    pob_analytic_group_id = fields.Many2one(
        string="PoB Analytic Group",
        comodel_name="account.analytic.group",
    )
    auto_create_pob_product_ids = fields.Many2many(
        string="Auto Create PoB Products",
        comodel_name="product.product",
        relation="rel_auto_create_pob_product_ids",
        column1="type_id",
        column2="product_id",
    )
    auto_create_pob_product_categ_ids = fields.Many2many(
        string="Auto Create PoB Product Categories",
        comodel_name="product.category",
        relation="auto_create_pob_product_categ_ids",
        column1="type_id",
        column2="categ_id",
    )
