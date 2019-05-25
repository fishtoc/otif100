from odoo import models, fields, api


class Plant(models.Model):
    _name = 'otif100.plant'

    name = fields.Char(
        string="Plant name",
    )
    company_id = fields.Char(  # Para filtrar por company
        required=True,
        store=True,
        readonly="1",
        default=lambda self: self.env.user.parent_id.name,
    )
    _sql_constraints = [
        ("name_unique",
         "UNIQUE(company_id)",
         "There must be only one plant")
    ]
    standard_dt = fields.Integer(
        string="Standard Delivery Time",
        help="Standard delivery time in working days for regular orders",
        default=20,
    )
    hours_day_1 = fields.Float(
        string="Hours per working day",
        default=8.0
    )
    plant_full = fields.Boolean(
        string="Full load",
        compute="_get_plant_status",
        help="If unmarked, you may want to anticipate the release of some orders",
    )
    min_buffer = fields.Integer(
        compute="_get_min_buffer",
    )

    @api.multi
    def _get_min_buffer(self):
        self.min_buffer = 5

    def _get_plant_status(self):  # Sumar carga liberada en CCRs en min_buffer días
        self.plant_full = True
