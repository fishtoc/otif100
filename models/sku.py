from odoo import models, fields, api


class Sku(models.Model):
    _name = 'otif100.sku'

    name = fields.Char(
        string="Product SKU",
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
    wo_sku = fields.One2many(
        comodel_name="otif100.work_order",
        inverse_name="sku_id",
        string="Product SKU",
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
         "SKU name must be unique")
    ]
