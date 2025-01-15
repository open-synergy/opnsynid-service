# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, models


class ServiceQuotation(models.Model):
    _name = "service.quotation"
    _inherit = [
        "service.quotation",
        "mixin.custom_info",
    ]
    _custom_info_create_page = True

    @api.onchange(
        "type_id",
    )
    def onchange_custom_info_template_id(self):
        self.custom_info_template_id = False
        if self.type_id:
            self.custom_info_template_id = self._get_template_custom_info()

    def _create_contract(self):
        self.ensure_one()
        _super = super(ServiceQuotation, self)
        _super._create_contract()
        contract = self.contract_id
        contract.custom_info_ids.unlink()
        contract.action_reload_custom_info_template()
        contract.clear_caches()
        CustomInfo = self.env["custom_info.value"]
        criteria = [
            ("model", "=", "service.contract"),
            ("res_id", "=", contract.id),
        ]
        for custom_info in CustomInfo.search(criteria):
            custom_info_property = custom_info.property_id
            criteria = [
                ("model", "=", "service.quotation"),
                ("res_id", "=", self.id),
                ("detail_id.property_id.id", "=", custom_info_property.id),
            ]
            sources = CustomInfo.search(criteria)
            if len(sources) > 0:
                custom_info.write(
                    {
                        "value_str": sources[0].value_str,
                        "value_float": sources[0].value_float,
                        "value_int": sources[0].value_int,
                        "value_date": sources[0].value_date,
                        "value_datetime": sources[0].value_datetime,
                        "value_id": sources[0].value_id
                        and sources[0].value_id.id
                        or False,
                        "value_ids": sources[0].value_ids
                        and [(6, 0, sources[0].value_ids.ids)]
                        or False,
                    }
                )
