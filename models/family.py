from odoo import models, fields, api


class Family(models.Model):
    _name = 'otif100.family'

    name = fields.Char(
        string="Production family",
        help="Production family for SKUs",
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
    company_id = fields.Char(  # Para filtrar por company
        required=True,
        store=True,
        readonly="1",
        default=lambda self: self.env.user.parent_id.name,
    )
    _sql_constraints = [
        ("name_unique",
         "UNIQUE(name)",
         "Family name must be unique"),
    ]
    espacio_derecha = fields.Char(  # En lista, para que buffer quede mejor
        string=" ",
        default="                                        ",
    )
