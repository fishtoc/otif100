from odoo import models, fields, api


class Family(models.Model):
    _name = 'otif100.family'

    name = fields.Char(
        string="Production family",
        help="Production family for SKUs"
    )
    buffer = fields.Integer(
        string="Buffer",
        default=10,
        help="Time buffer in days",
    )
    sku_ids = fields.One2many(
        comodel_name="otif100.sku",
        inverse_name="fam_id",
        string="Products SKUs",
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
         "Family name must be unique")
    ]
