# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ServiceContractFixItemPaymentTermDetail(models.Model):
    """
    Propagates the parent contract's Operating Unit to invoice lines.
    Overrides ``_prepare_invoice_line`` so every invoice line created
    from a payment term detail line carries the same operating unit as
    its ``service.contract``, keeping OU-scoped accounting entries
    consistent down to the line level.
    """

    _name = "service.contract_fix_item_payment_term_detail"
    _inherit = [
        "service.contract_fix_item_payment_term_detail",
    ]

    def _prepare_invoice_line(self):
        """Add ``operating_unit_id`` to the ``account.move.line`` values.

        Extension point: overridden here so the invoice line created
        from this detail line inherits the operating unit of the
        contract it belongs to
        (``self.term_id.service_id.operating_unit_id``).

        :return: dict of ``account.move.line`` values, with
            ``operating_unit_id`` set.
        """
        _super = super(ServiceContractFixItemPaymentTermDetail, self)
        result = _super._prepare_invoice_line()
        result.update(
            {
                "operating_unit_id": self.term_id.service_id.operating_unit_id.id,
            }
        )
        return result
