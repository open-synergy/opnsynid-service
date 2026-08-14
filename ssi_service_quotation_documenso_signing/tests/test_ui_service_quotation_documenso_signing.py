# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiServiceQuotationDocumensoSigning(HttpSavepointCase):
    """Tour tests for the ``service.quotation`` Documenso signing delta."""

    @classmethod
    def setUpClass(cls):
        """Create fixtures for both tours in this test class.

        One quotation is moved to ``confirm`` in Python
        (``action_confirm()`` with ``bypass_policy_check``), not via UI
        clicks, per Keputusan Desain (issue
        open-synergy/opnsynid-service#113). A second, separate
        quotation plus an active Documenso backend and signing
        template are created for the New Signing Request tour.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Tour SQ Documenso Partner",
                "is_company": True,
            }
        )
        cls.service_type = cls.env["service.type"].create(
            {
                "name": "Tour SQ Documenso Type",
                "code": "TOURSQDCTYPE",
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

        # Pre-Condition IK 05-approve.md (delta): record already Waiting
        # for Approval. The active approval template has no Documenso
        # Signing Template configured, so the Signature Requests tab is
        # present (``_documenso_signing_create_page = True``) but the
        # base Approve/OK Flow is unaffected -- this tour does not
        # exercise it.
        cls.quotation_approve = cls.env["service.quotation"].create(
            dict(base_values, title="Tour SQ Documenso Approve")
        )
        cls.quotation_approve.sudo().with_context(
            bypass_policy_check=True
        ).action_confirm()

        # Pre-Condition IK 06-create-signing-request.md: an active
        # documenso.backend and an active documenso.signing.template
        # (Source Model = service.quotation) must exist, plus a
        # service.quotation record whose form shows the Signature
        # Requests tab (any status -- the tab is unconditional).
        cls.quotation_signing_request = cls.env["service.quotation"].create(
            dict(base_values, title="Tour SQ Documenso Signing Request")
        )
        cls.documenso_backend = cls.env["documenso.backend"].create(
            {
                "name": "Tour SQ Documenso Backend",
                "base_url": "https://documenso.example.com",
                "api_key": "tour-test-api-key",
            }
        )
        # ``documenso.signature.request.py3o_report_id`` is required, and
        # the wizard copies it from the signing template's
        # ``py3o_report_id`` on confirm -- without a matching report the
        # create() call in ``action_confirm`` raises a validation error
        # and the wizard never closes. ``ssi_service_quotation`` ships no
        # py3o report of its own, so a minimal one is created here for
        # the tour's fixture only.
        cls.documenso_py3o_report = cls.env["ir.actions.report"].create(
            {
                "name": "Tour SQ Documenso Py3o Report",
                "model": "service.quotation",
                "report_name": ("ssi_service_quotation_documenso_signing.tour_report"),
                "report_type": "py3o",
                "py3o_filetype": "pdf",
            }
        )
        cls.documenso_signing_template = cls.env["documenso.signing.template"].create(
            {
                "name": "Tour SQ Documenso Signing Template",
                "code": "TOURSQDCST",
                "res_model": "service.quotation",
                "py3o_report_id": cls.documenso_py3o_report.id,
            }
        )

    def test_approve(self):
        """Run the approve tour for the Documenso signing delta.

        IK: docs/service_quotation/05-approve.md (E2a delta -- Modified
        Flow)
        """
        self.start_tour(
            "/web",
            "ssi_service_quotation_documenso_signing_service_quotation_approve",
            login="admin",
        )

    def test_create_signing_request(self):
        """Run the New Signing Request tour on ``service.quotation``.

        IK: docs/service_quotation/06-create-signing-request.md (E3 --
        new action). The tour stops once the new row appears on the
        Signature Requests page; it does not click into the created
        request's own form to send it to Documenso over the network.
        """
        self.start_tour(
            "/web",
            "ssi_service_quotation_documenso_signing_service_quotation"
            "_create_signing_request",
            login="admin",
        )
