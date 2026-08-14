# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ServiceQuotation(models.Model):
    """
    Adds automatic project creation defaults to won quotations.
    Ensures the ``service.contract`` generated when a quotation is
    marked Win inherits the same ``auto_create_project`` onchange
    default a user gets when manually picking Type on a new contract,
    since :meth:`_create_contract` builds the contract with ``new()``
    instead of going through the form's onchange chain.
    """

    _name = "service.quotation"
    _inherit = [
        "service.quotation",
    ]

    def _compute_contract_onchange(self, temp_record):
        """Extend the base onchange chain with the project default.

        Runs ``onchange_auto_create_project`` (added by
        ``ssi_service_project``) on the in-memory ``service.contract``
        record so its ``auto_create_project`` field is pre-filled from
        the quotation's Type before the contract is created.

        :param temp_record: ``service.contract`` in-memory record
            built with :meth:`~odoo.models.Model.new`.
        :return: the same ``temp_record``, with ``auto_create_project``
            filled in addition to the base onchanges.
        """
        _super = super(ServiceQuotation, self)
        _super._compute_contract_onchange(temp_record)
        temp_record.onchange_auto_create_project()
        return temp_record
