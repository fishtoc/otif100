from odoo import models, fields, api, exceptions
from datetime import timedelta


class Plant(models.Model):
    _name = 'otif100.plant'

    name = fields.Char(
        string="Production line name",
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
         "There must be only one production line")
    ]
    standard_dt = fields.Integer(
        string="Standard Delivery Time",
        help="Standard delivery time in working days for regular orders",
        default=20,
    )
    standard_pd = fields.Date(
        string="Suggested date to promise",
        compute="_get_standard_pd",
    )
    hours_day_1 = fields.Float(
        string="Hours per working day CCR 1",
        default=8.0,
    )
    hours_day_2 = fields.Float(
        string="Hours per working day CCR 2",
        default=8.0,
    )
    hours_day_3 = fields.Float(
        string="Hours per working day CCR 3",
        default=8.0,
    )
    load_front_1 = fields.Float(  # Load short horizon ~1/2 PBT
        string="Load CCR 1",
        help="Percentage of available capacity in half production buffer time",
        compute="_get_load_front_1",
    )
    load_front_2 = fields.Float(
        string="Load CCR 2",
        help="Percentage of available capacity in half production buffer time",
        compute="_get_load_front_2",
    )
    load_front_3 = fields.Float(
        string="Load CCR 3",
        help="Percentage of available capacity in half production buffer time",
        compute="_get_load_front_3",
    )
    plant_full = fields.Boolean(
        string="Full load",
        compute="_get_plant_status",
        help="If unmarked, you may want to anticipate the release of some orders",
    )
    early_release = fields.Char(
        string="Suggestion to exploit capacity",
        help="Should we release something earlier than Recommended Release Date?",
        compute="_get_release_status",
    )
    min_buffer = fields.Integer(
        string="Target WIP in working days",
        help="Number of days that you consider a healthy WIP for this line",
        default=5,
    )

    @api.depends("load_front_1", "load_front_2", "load_front_3")
    def _get_plant_status(self):
        self.plant_full = False
        if self.load_front_1 > 95 or self.load_front_2 > 95 or self.load_front_3 > 95:
            self.plant_full = True

    @api.depends("plant_full")
    def _get_release_status(self):
        if self.plant_full:
            self.early_release = "Do not release any order earlier than Recommended Release Date"
        else:
            self.early_release = "Release some orders until this message changes"

    @api.depends("min_buffer", "hours_day_1")
    def _get_load_front_1(self):
        self.load_front_1 = 0
        if self.min_buffer * self.hours_day_1 > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name)],
                ['hours_ccr_1'])
            hrs_wos = [i['hours_ccr_1'] for i in w_orders]
            hours_ccr = 0
            for hr_wo in hrs_wos:
                hours_ccr = hours_ccr + hr_wo
            self.load_front_1 = 100 * hours_ccr / \
                (self.min_buffer * self.hours_day_1)

    @api.depends("min_buffer", "hours_day_2")
    def _get_load_front_2(self):
        self.load_front_2 = 0
        if self.min_buffer * self.hours_day_2 > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name)],
                ['hours_ccr_2'])
            hrs_wos = [i['hours_ccr_2'] for i in w_orders]
            hours_ccr = 0
            for hr_wo in hrs_wos:
                hours_ccr = hours_ccr + hr_wo
            self.load_front_2 = 100 * hours_ccr / \
                (self.min_buffer * self.hours_day_2)

    @api.depends("min_buffer", "hours_day_3")
    def _get_load_front_3(self):
        self.load_front_3 = 0
        if self.min_buffer * self.hours_day_3 > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name)],
                ['hours_ccr_3'])
            hrs_wos = [i['hours_ccr_3'] for i in w_orders]
            hours_ccr = 0
            for hr_wo in hrs_wos:
                hours_ccr = hours_ccr + hr_wo
            self.load_front_3 = 100 * hours_ccr / \
                (self.min_buffer * self.hours_day_3)

    @api.depends("standard_dt")
    def _get_standard_pd(self):
        nw_days = self.env["otif100.nwd"].search_read(
            [('company_id', '=', self.env.user.parent_id.name)], ['nwds'])
        nw_dates = [i['nwds'] for i in nw_days]
        delivery_time = self.standard_dt
        s_dd_prom = fields.Date.today()
        while delivery_time > 0:
            s_dd_prom = s_dd_prom + timedelta(days=1)
            if s_dd_prom not in nw_dates:
                delivery_time = delivery_time - 1
        self.standard_pd = s_dd_prom
