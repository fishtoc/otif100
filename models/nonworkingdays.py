from odoo import models, fields, api


class Nonworkingdays(models.Model):
    _name = 'otif100.nwd'

    name = fields.Date(
        string="Non working day",
        help="A day to ignore when calculating dates"
    )
    description = fields.Char(
        string="Description",
        default="Weekend",
        help="A brief description of why it is not a working day",
    )
    company_id = fields.Many2one(  # Para filtrar por company
        comodel_name="res.partner",
        required=True,
        store=True,
        default=lambda self: self.env.user.partner_id,
    )
    _sql_constraints = [
        ("name_unique",
         "UNIQUE(name)",
         "This date is already marked as non working day")
    ]
