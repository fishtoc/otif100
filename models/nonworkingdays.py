from odoo import models, fields, api
import calendar


class Nonworkingdays(models.Model):
    _name = 'otif100.nwd'

    nwds = fields.Date(
        string="Non working day",
        help="A day to ignore when calculating dates",
        default=fields.Date.today(),
    )
    day_name = fields.Char(
        string="Day of week",
        compute="_get_dayofweek",
        store=True,
    )
    description = fields.Char(
        string="Description",
        default="Weekend",
        help="A brief description of why it is not a working day",
    )
    company_id = fields.Char(  # Para filtrar por company
        required=True,
        store=True,
        default=lambda self: self.env.user.parent_id.name,
    )

    @api.depends("nwds")
    def _get_dayofweek(self):
        days = list(calendar.day_name)
        for r in self:
            yy, mm, dd = r.nwds.year, r.nwds.month, r.nwds.day
            r.day_name = days[calendar.weekday(yy, mm, dd)]
