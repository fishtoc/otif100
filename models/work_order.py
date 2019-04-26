from odoo import models, fields, api
from datetime import timedelta


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
        required=True,
        ondelete="cascade",
        help="Your product code",

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
        default=None,
    )
    actual_release_date = fields.Date(
        string="Actual Release Date",
        default=None,
    )
    buffer = fields.Integer(
        string="Time buffer",
        related="sku_id.buffer",
    )
    recommended_release_date = fields.Date(
        compute="_get_recommended_release_date",
        string="Recommended Release Date",
    )
    should_be_released = fields.Boolean(
        compute="_should_release",
        string="Should be released",
    )
    buffer_penetration = fields.Float(
        compute="_get_buffer_penetration"
    )

    @api.depends("due_date", "buffer")
    def _get_recommended_release_date(self):
        for r in self:
            Buffer = timedelta(r.buffer)
            r.recommended_release_date = r.due_date - Buffer

    @api.depends("recommended_release_date")
    def _should_release(self):
        for r in self:
            if fields.Date.today() < r.recommended_release_date:
                r.should_be_released = False
            else:
                r.should_be_released = True

    @api.depends("recommended_release_date", "buffer")
    def _get_buffer_penetration(self):
        for r in self:
            Buffer_comsumption = (fields.Date.today() -
                                  r.recommended_release_date).days
            r.buffer_penetration = 100 * Buffer_comsumption / r.buffer
