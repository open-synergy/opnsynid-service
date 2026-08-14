# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. 14.0's plain HttpCase does not set up
# cls.env in setUpClass, so Pre-Condition fixtures below would fail with
# AttributeError before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiServiceContract(HttpSavepointCase):
    """Tour tests for the ``service.contract`` work instructions."""

    @classmethod
    def _to_confirm(cls, contract):
        """Move a draft contract to ``confirm``, creating approval records.

        :param contract: ``service.contract`` recordset in ``draft``.
        :return: None. Uses ``bypass_policy_check`` so the call does not
            depend on which user runs it; the approval records it
            creates still come from the approval template configuration
            (group *Service Contract — Validator*), so a later approve
            performed as ``base.user_admin`` (in that group) is genuine.
        """
        contract.sudo().with_context(bypass_policy_check=True).action_confirm()

    @classmethod
    def _force_state(cls, contract, state):
        """Set a contract's state directly, bypassing the workflow.

        :param contract: ``service.contract`` recordset.
        :param state: str, the target ``state`` value.
        :return: None. Used only to set up a tour's Pre-Condition
            starting state (``open``/``reject``) — the mixin has no
            ``state``-level constraint, and the tour under test only
            needs the record to genuinely be in that state, not to
            have arrived there through a fully simulated approval
            (which would require impersonating a specific approver
            outside the browser session the tour itself runs in).
        """
        contract.sudo().write({"state": state})

    @classmethod
    def setUpClass(cls):
        """Create the partner, type, and one contract per tour scenario.

        Each tour gets its own record in the state its IK Pre-Condition
        requires, so tours stay independent of each other.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "TOUR Service Partner",
                "is_company": True,
            }
        )
        cls.service_type = cls.env["service.type"].create(
            {
                "name": "TOUR Service Type",
                "code": "TOURSVC",
            }
        )
        # Radio options for the Cancel/Terminate wizards (10-cancel,
        # 11-terminate): without a reason marked global_use, the wizard
        # renders with zero radio options and the tour cannot pick one.
        cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR Cancel Reason",
                "code": "TOURCANCEL",
                "global_use": True,
            }
        )
        cls.env["base.terminate_reason"].create(
            {
                "name": "TOUR Terminate Reason",
                "code": "TOURTERMINATE",
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
        cls.contract_edit = cls.env["service.contract"].create(
            dict(base_values, title="TOUR SC Edit")
        )
        # 03-delete
        cls.contract_delete = cls.env["service.contract"].create(
            dict(base_values, title="TOUR SC Delete")
        )
        # 04-confirm (clicked live by the tour, stays in draft here)
        cls.contract_confirm = cls.env["service.contract"].create(
            dict(base_values, title="TOUR SC Confirm")
        )
        # 05-approve (clicked live by the tour; pre-moved to confirm)
        cls.contract_approve = cls.env["service.contract"].create(
            dict(base_values, title="TOUR SC Approve")
        )
        cls._to_confirm(cls.contract_approve)
        # 06-reject (clicked live by the tour; pre-moved to confirm)
        cls.contract_reject = cls.env["service.contract"].create(
            dict(base_values, title="TOUR SC Reject")
        )
        cls._to_confirm(cls.contract_reject)
        # 09-finish: open, with one payment term line to manage
        cls.contract_finish = cls.env["service.contract"].create(
            dict(
                base_values,
                title="TOUR SC Finish",
                fix_item_payment_term_ids=[
                    (0, 0, {"name": "TOUR Term Finish"}),
                ],
            )
        )
        cls._force_state(cls.contract_finish, "open")
        # 10-cancel (any state allows it; draft is the simplest)
        cls.contract_cancel = cls.env["service.contract"].create(
            dict(base_values, title="TOUR SC Cancel")
        )
        # 11-terminate: open
        cls.contract_terminate = cls.env["service.contract"].create(
            dict(base_values, title="TOUR SC Terminate")
        )
        cls._force_state(cls.contract_terminate, "open")
        # 12-restart: rejected
        cls.contract_restart = cls.env["service.contract"].create(
            dict(base_values, title="TOUR SC Restart")
        )
        cls._force_state(cls.contract_restart, "reject")
        # 13-reset-number: give it a non-"/" name first, so the tour's
        # Post-Condition assertion (name back to "/") only becomes true
        # after Reset Document Number actually runs, not before.
        cls.contract_reset = cls.env["service.contract"].create(
            dict(base_values, title="TOUR SC Reset")
        )
        cls.contract_reset.sudo().write({"name": "TOUR/RESET/000001"})

    def test_create(self):
        """Run the create tour for ``service.contract``.

        IK: docs/service_contract/01-create.md
        """
        self.start_tour("/web", "ssi_service_service_contract_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``service.contract``.

        IK: docs/service_contract/02-edit.md
        """
        self.start_tour("/web", "ssi_service_service_contract_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``service.contract``.

        IK: docs/service_contract/03-delete.md
        """
        self.start_tour("/web", "ssi_service_service_contract_delete", login="admin")

    def test_confirm(self):
        """Run the confirm tour for ``service.contract``.

        IK: docs/service_contract/04-confirm.md
        """
        self.start_tour("/web", "ssi_service_service_contract_confirm", login="admin")

    def test_approve(self):
        """Run the approve tour for ``service.contract``.

        IK: docs/service_contract/05-approve.md
        """
        self.start_tour("/web", "ssi_service_service_contract_approve", login="admin")

    def test_reject(self):
        """Run the reject tour for ``service.contract``.

        IK: docs/service_contract/06-reject.md
        """
        self.start_tour("/web", "ssi_service_service_contract_reject", login="admin")

    def test_finish(self):
        """Run the finish tour for ``service.contract``.

        IK: docs/service_contract/09-finish.md
        """
        self.start_tour("/web", "ssi_service_service_contract_finish", login="admin")

    def test_cancel(self):
        """Run the cancel tour for ``service.contract``.

        IK: docs/service_contract/10-cancel.md
        """
        self.start_tour("/web", "ssi_service_service_contract_cancel", login="admin")

    def test_terminate(self):
        """Run the terminate tour for ``service.contract``.

        IK: docs/service_contract/11-terminate.md
        """
        self.start_tour("/web", "ssi_service_service_contract_terminate", login="admin")

    def test_restart(self):
        """Run the restart tour for ``service.contract``.

        IK: docs/service_contract/12-restart.md
        """
        self.start_tour("/web", "ssi_service_service_contract_restart", login="admin")

    def test_reset_number(self):
        """Run the reset document number tour for ``service.contract``.

        IK: docs/service_contract/13-reset-number.md
        """
        self.start_tour(
            "/web", "ssi_service_service_contract_reset_number", login="admin"
        )
