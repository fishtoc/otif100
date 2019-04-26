from odoo import models, fields, api


class Sku(models.Model):
    _name = 'otif100.sku'

    sku_id = fields.Char(
        string="SKU",
        help="Your SKU code"
    )
    fam_id = fields.Many2one(
        comodel_name="otif100.family",
        ondelete="cascade",
        string="Production family",
        required=True,
        help="Family of this SKU",
    )
    buffer = fields.Integer(
        related="fam_id.buffer",
        string="Time buffer",
    )
