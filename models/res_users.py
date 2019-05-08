from odoo import models, fields, api


class Users(models.Model):
    _inherit = 'res.users'

    parent_id = fields.Many2one(  # Para filtrar por company
        comodel_name="res.partner",
    )
