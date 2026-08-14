# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. 14.0's plain HttpCase does not set up
# cls.env in setUpClass, so Pre-Condition fixtures below would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiServiceQuotation(HttpSavepointCase):
    """Tour tests for the ``service.quotation`` work instructions."""

    @classmethod
    def _to_confirm(cls, quotation):
        """Move a draft quotation to ``confirm``, creating approvals.

        :param quotation: ``service.quotation`` recordset in ``draft``.
        :return: None. Uses ``bypass_policy_check`` so the call does not
            depend on which user runs it; the approval records it
            creates still come from the approval template configuration
            (group *Service Quotation — Validator*), so a later approve
            performed as ``base.user_admin`` (in that group) is genuine.
        """
        quotation.sudo().with_context(bypass_policy_check=True).action_confirm()

    @classmethod
    def _force_state(cls, quotation, state):
        """Set a quotation's state directly, bypassing the workflow.

        :param quotation: ``service.quotation`` recordset.
        :param state: str, the target ``state`` value.
        :return: None. Used only to set up a tour's Pre-Condition
            starting state (``open``/``cancel``/``reject``) — the mixin
            has no ``state``-level constraint, and the tour under test
            only needs the record to genuinely be in that state, not to
            have arrived there through a fully simulated approval
            (which would require impersonating a specific approver
            outside the browser session the tour itself runs in).
        """
        quotation.sudo().write({"state": state})

    @classmethod
    def setUpClass(cls):
        """Create the partner, type, and one quotation per tour scenario.

        Each tour gets its own record in the state its IK Pre-Condition
        requires, so tours stay independent of each other.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "TOUR Service Quotation Partner",
                "is_company": True,
            }
        )
        cls.service_type = cls.env["service.type"].create(
            {
                "name": "TOUR Service Quotation Type",
                "code": "TOURSQTYPE",
            }
        )
        # Radio option for the Cancel wizard (09-cancel): without a
        # reason marked global_use, the wizard renders with zero radio
        # options and the tour cannot pick one.
        cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR SQ Cancel Reason",
                "code": "TOURSQCANCEL",
                "global_use": True,
            }
        )
        # Radio option for the Lost wizard (08-lost): without a reason
        # marked global_use, the wizard renders with zero radio options
        # and the tour cannot pick one (see IrModel._compute_all_
        # lost_reason_ids in ssi_transaction_win_lost_mixin).
        cls.env["base.lost_reason"].create(
            {
                "name": "TOUR SQ Lost Reason",
                "code": "TOURSQLOST",
                "global_use": True,
            }
        )
        base_values = {
            "partner_id": cls.partner.id,
            "type_id": cls.service_type.id,
            "manager_id": cls.admin.id,
            "salesperson_id": cls.admin.id,
            "date": "2026-01-01",
            "date_start": "2026-01-01",
            "date_end": "2026-12-31",
            "currency_id": cls.env.ref("base.USD").id,
            "pricelist_id": cls.env.ref("product.list0").id,
        }

        # 02-edit
        cls.quotation_edit = cls.env["service.quotation"].create(
            dict(base_values, title="TOUR SQ Edit")
        )
        # 03-delete
        cls.quotation_delete = cls.env["service.quotation"].create(
            dict(base_values, title="TOUR SQ Delete")
        )
        # 04-confirm (clicked live by the tour, stays in draft here)
        cls.quotation_confirm = cls.env["service.quotation"].create(
            dict(base_values, title="TOUR SQ Confirm")
        )
        # 05-approve (clicked live by the tour; pre-moved to confirm)
        cls.quotation_approve = cls.env["service.quotation"].create(
            dict(base_values, title="TOUR SQ Approve")
        )
        cls._to_confirm(cls.quotation_approve)
        # 06-reject (clicked live by the tour; pre-moved to confirm)
        cls.quotation_reject = cls.env["service.quotation"].create(
            dict(base_values, title="TOUR SQ Reject")
        )
        cls._to_confirm(cls.quotation_reject)
        # 07-win: open
        cls.quotation_win = cls.env["service.quotation"].create(
            dict(base_values, title="TOUR SQ Win")
        )
        cls._force_state(cls.quotation_win, "open")
        # 08-lost: open
        cls.quotation_lost = cls.env["service.quotation"].create(
            dict(base_values, title="TOUR SQ Lost")
        )
        cls._force_state(cls.quotation_lost, "open")
        # 09-cancel (any listed state allows it; draft is the simplest)
        cls.quotation_cancel = cls.env["service.quotation"].create(
            dict(base_values, title="TOUR SQ Cancel")
        )
        # 10-restart: rejected
        cls.quotation_restart = cls.env["service.quotation"].create(
            dict(base_values, title="TOUR SQ Restart")
        )
        cls._force_state(cls.quotation_restart, "reject")

    def test_create(self):
        """Run the create tour for ``service.quotation``.

        IK: docs/service_quotation/01-create.md
        """
        self.start_tour(
            "/web", "ssi_service_quotation_service_quotation_create", login="admin"
        )

    def test_edit(self):
        """Run the edit tour for ``service.quotation``.

        IK: docs/service_quotation/02-edit.md
        """
        self.start_tour(
            "/web", "ssi_service_quotation_service_quotation_edit", login="admin"
        )

    def test_delete(self):
        """Run the delete tour for ``service.quotation``.

        IK: docs/service_quotation/03-delete.md
        """
        self.start_tour(
            "/web", "ssi_service_quotation_service_quotation_delete", login="admin"
        )

    def test_confirm(self):
        """Run the confirm tour for ``service.quotation``.

        IK: docs/service_quotation/04-confirm.md
        """
        self.start_tour(
            "/web", "ssi_service_quotation_service_quotation_confirm", login="admin"
        )

    def test_approve(self):
        """Run the approve tour for ``service.quotation``.

        IK: docs/service_quotation/05-approve.md
        """
        self.start_tour(
            "/web", "ssi_service_quotation_service_quotation_approve", login="admin"
        )

    def test_reject(self):
        """Run the reject tour for ``service.quotation``.

        IK: docs/service_quotation/06-reject.md
        """
        self.start_tour(
            "/web", "ssi_service_quotation_service_quotation_reject", login="admin"
        )

    def test_win(self):
        """Run the win tour for ``service.quotation``.

        IK: docs/service_quotation/07-win.md
        """
        self.start_tour(
            "/web", "ssi_service_quotation_service_quotation_win", login="admin"
        )

    def test_lost(self):
        """Run the lost tour for ``service.quotation``.

        IK: docs/service_quotation/08-lost.md
        """
        self.start_tour(
            "/web", "ssi_service_quotation_service_quotation_lost", login="admin"
        )

    def test_cancel(self):
        """Run the cancel tour for ``service.quotation``.

        IK: docs/service_quotation/09-cancel.md
        """
        self.start_tour(
            "/web", "ssi_service_quotation_service_quotation_cancel", login="admin"
        )

    def test_restart(self):
        """Run the restart tour for ``service.quotation``.

        IK: docs/service_quotation/10-restart.md
        """
        self.start_tour(
            "/web", "ssi_service_quotation_service_quotation_restart", login="admin"
        )
