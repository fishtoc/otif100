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
