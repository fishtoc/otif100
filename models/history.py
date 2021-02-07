from odoo import models, fields, api, exceptions
from datetime import timedelta


class History(models.Model):
    _name = 'otif100.history'

    wo_id = fields.Char(
        string='Work order',
        required=True,
    )
    cli_id = fields.Char(
        string='Customer',
    )
    sku_id = fields.Char(
        string='Product Code',
        help="Your product code",
    )
    sku_description = fields.Char(  # It allows different descriptions for same sku
        string='Product description',
        default='',
        help='Custom description for this work order',
    )
    qty_total = fields.Float(
        string="Total qty",
        default=0.0,
    )
    due_date = fields.Date(
        string="Due Date",
        default=fields.Date.today() + timedelta(days=30),
    )
    actual_release_date = fields.Date(
        string="Actual Release Date",
        default=None,
    )
    finish_date = fields.Date(
        string="Finish date",
    )
    company_id = fields.Char(  # Para filtrar por company
    )
    buffer_status = fields.Char(
        compute="_get_buffer_status",
        string="Buffer color",
        store=True,
    )
    order_type = fields.Char(
        compute="_get_type",
        string="Type",
        help="MTO: Make to Order - MTA: Make to Availability",
        store=True,
    )
    ontime = fields.Float(
        string="OTIF",
        help="Percentage of OTIF",
        group_operator="avg",
    )
