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
    work_center = fields.Char(
        string="Work center",
        default="",
        help="Usually the work center where most of the order is now",
    )
    due_date = fields.Date(
        string="Due Date",
        default=fields.Date.today() + timedelta(days=30),
    )
    actual_release_date = fields.Date(
        string="Actual Release Date",
        default=None,
    )
    buffer = fields.Integer(
        string="Time buffer",
        related="sku_id.buffer",
    )
    company_id = fields.Char(  # Para filtrar por company
        required=True,
        store=True,
        default=lambda self: self.env.user.parent_id.name,
    )
    _sql_constraints = [  # ****** REVISAR SI constrains o esto
        ("name_unique",
         "UNIQUE(wo_id)",
         "Work order identifier must be unique")
    ]
    recommended_release_date = fields.Date(
        compute="_get_recommended_release_date",
        string="Recommended Release Date",
        store=True,
    )
    should_be_released = fields.Boolean(
        compute="_should_release",
        string="Should be released",
        store=True,
    )
    buffer_penetration = fields.Float(
        compute="_get_buffer_penetration",
        default=0,
        store=True,
    )
    buffer_status = fields.Char(
        string="Buffer color",
        compute="_get_buffer_status",
        store=True,
    )
    is_released = fields.Boolean(
        compute="_check_released",
        string="Already released",
        store=True,
    )
    action_to_take = fields.Char(
        compute="_get_action",
        string="DO THIS",
        help="Obey this instruction and you will get 100% On Time In Full... Believe it or not!!",
    )
    need_action = fields.Boolean(
        compute="_check_action",
        default=False,
        string="NEED ATTENTION",
        store=True,
    )

    @api.depends("due_date", "buffer")
    def _get_recommended_release_date(self):  # ******** FIX, por ahora
        # model = self.pool.get("otif100.nwd")        # días múltiplos de 7
        # nw_days = model.search([('company_id', '=', 'self.company_id')])
        nw_days = []
        cur_date = fields.Date.to_date("2019-01-01")
        while cur_date < fields.Date.to_date("2020-01-01"):
            if (cur_date.day % 7) == 0:
                nw_days.append(cur_date)
            cur_date = cur_date + timedelta(days=1)
        for r in self:
            buff = r.buffer
            recc_rd = r.due_date
            while buff > 0:
                recc_rd = recc_rd - timedelta(days=1)
                if recc_rd not in nw_days:
                    buff = buff - 1
                r.recommended_release_date = recc_rd

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
            if r.buffer > 0:
                Buffer_comsumption = (fields.Date.today() -
                                      r.recommended_release_date).days
                r.buffer_penetration = 100 * Buffer_comsumption / r.buffer

    @api.depends("buffer_penetration")
    def _get_buffer_status(self):
        for r in self:
            if r.buffer_penetration < 0:
                r.buffer_status = 'cyan'
            elif r.buffer_penetration < 33.01:
                r.buffer_status = 'green'
            elif r.buffer_penetration < 66.01:
                r.buffer_status = 'yellow'
            elif r.buffer_penetration < 100.01:
                r.buffer_status = 'red'
            else:
                r.buffer_status = 'black'

    @api.depends("actual_release_date")
    def _check_released(self):
        for r in self:
            r.is_released = r.actual_release_date

    @api.depends("should_be_released", "is_released")
    def _get_action(self):
        for r in self:
            if r.is_released and not r.should_be_released:
                r.action_to_take = 'FREEZE THIS ORDER NOW'
            elif not r.is_released and r.should_be_released:
                r.action_to_take = 'RELEASE THIS ORDER ASAP'
            elif not r.is_released and not r.should_be_released:
                r.action_to_take = 'DO NOT PROCESS YET'
            else:
                r.action_to_take = 'PROCESS ACCORDING TO ITS COLOR'

    @api.depends("action_to_take")
    def _check_action(self):
        for r in self:
            if r.action_to_take != 'PROCESS ACCORDING TO ITS COLOR' and r.action_to_take != 'DO NOT PROCESS YET':
                r.need_action = True
            else:
                r.need_action = False
