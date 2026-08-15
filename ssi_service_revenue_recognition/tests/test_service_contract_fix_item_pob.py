# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestServiceContractFixItemPob(YamlTransactionCase):
    """Covers ``service.contract_fix_item.action_create_pob``.

    ``service.contract_fix_item`` is a SQL view (see
    ``ssi_service.models.service_contract_fix_item``) that groups the
    underlying payment term detail rows by
    ``product_id, product_category_id, name, price_unit, uom_id``. Two
    detail lines for the *same* product but *different* price therefore
    surface as two distinct view rows -- but ``_compute_pob_id`` used to
    search for an existing Performance Obligation by ``product_id`` alone,
    so the second row silently linked to the first row's PoB instead of
    getting its own, understating the contract's total Performance
    Obligation by the second row's amount (OFS/26/000023).

    Also covers OFS/26/000026's full history: ``_prepare_pob_data``
    originally assigned the line's ``amount_untaxed`` (already
    quantity-multiplied) to the PoB's own ``price_unit``, which was
    changed to the line's own (tax-inclusive) ``price_unit`` field, then
    reverted back to ``amount_untaxed`` on the same ticket -- accepting
    that ``price_subtotal`` (``price_unit * uom_quantity``) would
    overstate the total for lines with quantity != 1. Real usage on
    contract SVC/2026/000001 (a quantity=2 line) then hit exactly that
    overstatement, so the ticket was reopened: the PoB's ``price_unit``
    must be the line's **per-unit untaxed** price -- neither the raw
    (tax-inclusive) contract ``price_unit`` nor the line's full
    (quantity-multiplied) ``amount_untaxed`` -- so that
    ``price_subtotal`` matches ``amount_untaxed`` again regardless of
    quantity. See ``_get_pob_price_unit`` in
    ``service_contract_fix_item.py``.

    Also covers OFS/26/000024's reopened complaint: ``_compute_pob_id``
    matched ``price_unit`` with a raw, unrounded division result
    against the PoB's own (currency-rounded) stored value, so a line
    whose untaxed amount does not divide evenly by its quantity never
    found its own already-created PoB.
    """

    def test_service_contract_fix_item_pob(self):
        """Run the PoB creation scenarios for ``service.contract_fix_item``."""
        self.run_yaml_scenario("test_data_service_contract_fix_item_pob.yaml")
