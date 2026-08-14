# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — NOT HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiServiceContract(HttpSavepointCase):
    """Tour test for the Documenso Signature Requests page on Approve."""

    @classmethod
    def setUpClass(cls):
        """Create one confirmed ``service.contract`` fixture for the tour.

        ``service_contract_validator_group`` already grants
        ``base.user_admin`` membership by default (see ``ssi_service``'s
        ``security/res_group_data.xml``), so ``admin`` can both open and
        approve the fixture without any extra group setup. The record's
        ``user_id`` is set explicitly to ``admin`` — ``cls.env`` runs as
        SUPERUSER here, and the record rule
        ``service_contract_internal_user_rule`` would otherwise hide it
        from the ``admin`` tour session.

        No ``approval.template`` with a Documenso signing template is
        configured here — that is server-side Documenso connector setup,
        out of scope for this module's IK/tour (Ruang Lingkup). The
        shipped default template therefore drives approval normally, and
        the tour proves the added Signature Requests page renders
        alongside that unchanged base flow.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        partner = cls.env["res.partner"].create(
            {"name": "TOUR DS SC Partner", "is_company": True}
        )
        service_type = cls.env["service.type"].create(
            {"name": "TOUR DS SC Type", "code": "TOURDS"}
        )
        cls.rec_approve = cls.env["service.contract"].create(
            {
                "partner_id": partner.id,
                "type_id": service_type.id,
                "manager_id": cls.admin.id,
                "salesperson_id": cls.admin.id,
                "pricelist_id": cls.env.ref("product.list0").id,
                "currency_id": cls.env.ref("base.USD").id,
                "date": "2026-01-01",
                "date_start": "2026-01-01",
                "date_end": "2026-12-31",
                "title": "TOUR-DS-SC-APPROVE",
                "user_id": cls.admin.id,
            }
        )
        cls.rec_approve.with_user(cls.admin).action_confirm()
        cls.rec_approve.invalidate_cache()

    def test_approve(self):
        """Run the approve tour for ``service.contract``.

        IK: docs/service_contract/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_service_documenso_signing_service_contract_approve",
            login="admin",
        )
