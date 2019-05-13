from odoo import models, fields, api, exceptions


class Wizard(models.TransientModel):
    inherit = "Work_order"
    _name = "otif100.wizard"

    def _get_default_work_orders(self):
        return self.env["otif100.work_order"].browse(self._context.get("active_ids"))

    @api.multi
    def recalculate(self):
        raise exceptions.ValidationError(
            "This function will soon be available.")
        return {}
