from odoo import models, fields, api


class Work_order(models.Model):
    _name = 'otif100.work_order'

    wo_id = fields.Char(
        string='Work order',
        required=True,
    )
    cli_id = fields.Char(
        string='Customer',
    )
    sku_id = fields.Many2one(
        comodel_name="otif100.sku",
        string='Product SKU',
        delegate=True,
        required=True,
    )
    qty_total = fields.Float(
        string="Total qty",
        default=0.0,
    )
    qty_pending = fields.Float(
        string="Pending qty",
        default=0.0,
    )
    due_date = fields.Date(
        string="Due Date",
        default=fields.Date.today,
    )
    actual_release_date = fields.Date(
        string="Actual Release Date",
        default=None,
    )
    buffer = fields.Integer(
        string="Time buffer",
        related="sku_id.buffer",
    )
