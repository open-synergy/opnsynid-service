# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class ServiceContract(models.Model):
    """
    Adds project.project integration to the service contract.
    Lets a contract auto-create (or refresh) a linked project once it
    reaches the open state, so project tracking can start without a
    separate manual step.
    """

    _name = "service.contract"
    _inherit = [
        "service.contract",
    ]

    auto_create_project = fields.Boolean(
        string="Auto Create Project",
        copy=True,
    )
    project_id = fields.Many2one(
        string="Project",
        comodel_name="project.project",
        copy=False,
    )

    @ssi_decorator.post_open_action()
    def _11_create_project(self):
        """Create or refresh the linked project when the contract opens.

        Runs after the contract reaches the ``open`` state (triggered
        by ``action_approve_approval``). If **Project** is already
        set, that project is refreshed with :meth:`_prepare_project_data`.
        Otherwise, when **Auto Create Project** is checked, a new
        ``project.project`` is created and linked via **Project**.
        """
        self.ensure_one()
        if self.project_id:
            self.project_id.write(self._prepare_project_data())
        elif not self.project_id and self.auto_create_project:
            Project = self.env["project.project"]
            project = Project.create(self._prepare_project_data())
            self.write(
                {
                    "project_id": project.id,
                }
            )

    def _prepare_project_data(self):
        """Build the ``project.project`` values for this contract.

        Extension point: override to add or change the fields copied
        from the contract onto the generated/refreshed project.

        :return: dict of ``project.project`` values
        """
        self.ensure_one()
        return {
            "name": self.title,
            "code": self.name,
            "user_id": self.manager_id.id,
            "partner_id": self.partner_id.id,
            "analytic_account_id": self.analytic_account_id.id,
            "date_start": self.date_start,
            "date": self.date_end,
        }

    @api.onchange("type_id")
    def onchange_auto_create_project(self):
        if self.type_id:
            self.auto_create_project = self.type_id.auto_create_project
