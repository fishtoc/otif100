from odoo import models, fields, api, exceptions
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
        string='Product Code',
        required=True,
        ondelete="cascade",
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
    qty_before_1 = fields.Float(  # Qty not processed by CCRi
        string="Qty before CCR 1",
        default=0.0,
    )
    parts_per_hour_1 = fields.Float(
        related="sku_id.parts_per_hour_1",
    )
    hours_ccr_1 = fields.Float(
        compute="_get_hours_ccr_1",
    )
    total_hours_ccr_1 = fields.Float(
        compute="_get_total_hours_ccr_1",
    )
    qty_before_2 = fields.Float(
        string="Qty before CCR 2",
        default=0.0,
    )
    parts_per_hour_2 = fields.Float(
        related="sku_id.parts_per_hour_2",
    )
    hours_ccr_2 = fields.Float(
        compute="_get_hours_ccr_2",
    )
    total_hours_ccr_2 = fields.Float(
        compute="_get_total_hours_ccr_2",
    )
    qty_before_3 = fields.Float(
        string="Qty before CCR 3",
        default=0.0,
    )
    parts_per_hour_3 = fields.Float(
        related="sku_id.parts_per_hour_3",
    )
    hours_ccr_3 = fields.Float(
        compute="_get_hours_ccr_3",
    )
    total_hours_ccr_3 = fields.Float(
        compute="_get_total_hours_ccr_3",
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
    stock_buffer = fields.Float(
        string="Stock buffer",
        default=0.0,
    )
    onhand = fields.Float(
        string="Stock",
        default=0.0,
    )
    company_id = fields.Char(  # Para filtrar por company
        required=True,
        store=True,
        readonly="1",
        default=lambda self: self.env.user.parent_id.name,
    )
    _sql_constraints = [
        ("name_unique",
         "UNIQUE(wo_id,company_id)",
         "Work order identifier must be unique")
    ]
    recommended_release_date = fields.Date(
        compute="_get_recommended_release_date",
        string="Scheduled Release Date",
        store=False,
    )
    should_be_released = fields.Boolean(
        compute="_should_release",
        string="Should be released",
        store=False,
    )
    buffer_penetration = fields.Float(
        compute="_get_buffer_penetration",
        default=0,
        store=False,
    )
    buffer_status = fields.Char(
        compute="_get_buffer_status",
        string="Buffer color",
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
        string="ALERT",
        store=True,
    )
    order_type = fields.Char(
        compute="_get_type",
        string="Type",
        help="MTO: Make to Order - MTA: Make to Availability",
        store=True,
    )
    today = fields.Date(
        compute="_get_today_date",
        store=False,
    )

    @api.depends("due_date", "buffer")
    def _get_recommended_release_date(self):
        nw_days = self.env["otif100.nwd"].search_read(
            [('company_id', '=', self.env.user.parent_id.name)], ['nwds'])
        nw_dates = [i['nwds'] for i in nw_days]
        for r in self:
            if r.order_type == "MTO":
                buff = r.buffer
                recc_rd = r.due_date
                while buff > 0:
                    recc_rd = recc_rd - timedelta(days=1)
                    if recc_rd not in nw_dates:
                        buff = buff - 1
                r.recommended_release_date = recc_rd

    @api.depends("recommended_release_date", "today")
    def _should_release(self):
        for r in self:
            if r.today < r.recommended_release_date:
                r.should_be_released = False
            else:
                r.should_be_released = True

    @api.depends("stock_buffer")
    def _get_type(self):
        for r in self:
            if r.stock_buffer > 0:
                r.order_type = "MTA"
                r.actual_release_date = r.today
                r.cli_id = "STOCK"
            else:
                r.order_type = "MTO"

    @api.depends("recommended_release_date", "buffer", "today", "stock_buffer", "onhand")
    def _get_buffer_penetration(self):
        nw_days = self.env["otif100.nwd"].search_read(
            [('company_id', '=', self.env.user.parent_id.name)], ['nwds'])
        nw_dates = [i['nwds'] for i in nw_days]
        for r in self:
            if r.stock_buffer > 0:
                r.buffer_penetration = 100 * (1 - r.onhand / r.stock_buffer)
            else:
                Buffer_comsumption = 0
                if r.buffer > 0:
                    cur_date = r.recommended_release_date
                    if cur_date <= r.today:
                        lapso = 1
                    else:
                        lapso = -1
                    while cur_date != r.today:
                        if cur_date not in nw_dates:
                            Buffer_comsumption = Buffer_comsumption + lapso
                        cur_date = cur_date + timedelta(days=lapso)
                    r.buffer_penetration = 100 * Buffer_comsumption / r.buffer

    @api.depends("buffer_penetration", "is_released", "due_date", "today")
    def _get_buffer_status(self):
        for r in self:
            if r.buffer_penetration < 0:
                if r.is_released:
                    r.buffer_status = '3. green'  # Para no confundir en piso
                else:
                    r.buffer_status = '4. cyan'
            elif r.buffer_penetration < 33.01:
                r.buffer_status = '3. green'
            elif r.buffer_penetration < 66.01:
                r.buffer_status = '2. yellow'
            elif r.buffer_penetration < 100.01:
                r.buffer_status = '1. red'
            else:
                r.buffer_status = '0. black'
            if r.order_type == "MTO" and r.due_date < r.today:
                r.buffer_status = '0. black'

    @api.depends("actual_release_date")
    def _check_released(self):
        for r in self:
            r.is_released = r.actual_release_date

    @api.depends("should_be_released", "is_released", "order_type")
    def _get_action(self):
        for r in self:
            r.action_to_take = 'PROCESS ACCORDING TO ITS COLOR'
            if r.order_type == "MTO":
                if r.is_released and not r.should_be_released:
                    r.action_to_take = 'FREEZE UNLESS RELEASED BY LOAD CONTROL'
                elif not r.is_released and r.should_be_released:
                    r.action_to_take = 'RELEASE THIS ORDER ASAP'
                elif not r.is_released and not r.should_be_released:
                    r.action_to_take = 'DO NOT PROCESS YET'

    @api.depends("action_to_take")
    def _check_action(self):
        for r in self:
            if r.action_to_take != 'PROCESS ACCORDING TO ITS COLOR' and r.action_to_take != 'DO NOT PROCESS YET':
                r.need_action = True
            else:
                r.need_action = False

    @api.multi
    def _get_today_date(self):
        for r in self:
            r.today = fields.Date.today()

    @api.depends("is_released", "total_hours_ccr_1")
    def _get_hours_ccr_1(self):
        for r in self:
            r.hours_ccr_1 = 0
            if r.is_released:
                r.hours_ccr_1 = r.total_hours_ccr_1

    @api.depends("is_released", "total_hours_ccr_2")
    def _get_hours_ccr_2(self):
        for r in self:
            r.hours_ccr_2 = 0
            if r.is_released:
                r.hours_ccr_2 = r.total_hours_ccr_2

    @api.depends("is_released", "total_hours_ccr_3")
    def _get_hours_ccr_3(self):
        for r in self:
            r.hours_ccr_3 = 0
            if r.is_released:
                r.hours_ccr_3 = r.total_hours_ccr_3

    @api.depends("qty_before_1")
    def _get_total_hours_ccr_1(self):
        for r in self:
            r.total_hours_ccr_1 = 0
            if r.parts_per_hour_1 > 0:
                r.total_hours_ccr_1 = r.qty_before_1 / r.parts_per_hour_1

    @api.depends("qty_before_2")
    def _get_total_hours_ccr_2(self):
        for r in self:
            r.total_hours_ccr_2 = 0
            if r.parts_per_hour_2 > 0:
                r.total_hours_ccr_2 = r.qty_before_2 / r.parts_per_hour_2

    @api.depends("qty_before_3")
    def _get_total_hours_ccr_3(self):
        for r in self:
            r.total_hours_ccr_3 = 0
            if r.parts_per_hour_3 > 0:
                r.total_hours_ccr_3 = r.qty_before_3 / r.parts_per_hour_3

    @api.multi
    def mass_release(self):
        today_date = fields.Date.today()
        worecs = self.env['otif100.work_order'].browse(
            self._context.get('active_ids'))
        for worec in worecs:
            worec.write({'actual_release_date': today_date, })
        return {}

    @api.multi
    def mass_freeze(self):
        worecs = self.env['otif100.work_order'].browse(
            self._context.get('active_ids'))
        for worec in worecs:
            worec.write({'actual_release_date': None, })
        return {}

    @api.multi
    def mass_finish_order(self):
        worecs = self.env['otif100.work_order'].browse(
            self._context.get('active_ids'))
        oldwos = self.env['otif100.history']
        for worec in worecs:
            # Construimos el registro nuevo
            ontime = 0
            if worec.order_type == 'MTO' and worec.due_date > fields.Date.today():
                ontime = 100
            elif worec.order_type == 'MTA' and worec.buffer_status != "0. black":
                ontime = 100
            upd_rec = {
                'wo_id': worec.wo_id, 
                'cli_id': worec.cli_id, 
                'sku_id': worec.sku_id.name,
                'sku_description': worec.sku_description, 
                'qty_total': worec.qty_total,
                'due_date': worec.due_date, 
                'actual_release_date': worec.actual_release_date,
                'company_id': worec.company_id, 
                'buffer_status': worec.buffer_status,
                'order_type': worec.order_type, 
                'ontime': ontime,
                'finish_date': fields.Date.today(),
            }
            # Revisa si existe en la historia
            saved_wos = oldwos.search([('wo_id','=',worec.wo_id)])
            # Si existe, actualiza; sino, lo crea
            if saved_wos:
                for saved_wo in saved_wos:
                    saved_wo.write(upd_rec)
            else:
                oldwos.create(upd_rec)
            worec.unlink()
        return {}

    @api.model
    def recalculate_colors(self):
        model = self.env['otif100.work_order']
        self.env.add_todo(model._fields['buffer_status'],
                          model.search([('order_type', '=', 'MTO')]))
        model.recompute()
        self.env.add_todo(model._fields['need_action'],
                          model.search([('order_type', '=', 'MTO')]))
        model.recompute()
        self.env.cr.commit()
