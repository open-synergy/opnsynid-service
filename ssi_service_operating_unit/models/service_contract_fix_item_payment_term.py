# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ServiceContractFixItemPaymentTerm(models.Model):
    """
    Propagates the parent contract's Operating Unit to generated invoices.
    Overrides ``_prepare_invoice_data`` so every invoice created from a
    payment term line carries the same operating unit as its
    ``service.contract``, keeping OU-scoped accounting entries consistent.
    """

    _name = "service.contract_fix_item_payment_term"
    _inherit = ["service.contract_fix_item_payment_term"]

    def _prepare_invoice_data(self):
        """Add ``operating_unit_id`` to the ``account.move`` values.

        Extension point: overridden here so the invoice created from
        this payment term inherits the operating unit of the contract
        it belongs to (``self.service_id.operating_unit_id``).

        :return: dict of ``account.move`` values, with
            ``operating_unit_id`` set.
        """
        _super = super(ServiceContractFixItemPaymentTerm, self)

        result = _super._prepare_invoice_data()
        result.update(
            {
                "operating_unit_id": self.service_id.operating_unit_id.id,
            }
        )
        return result
