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
         "There can be only one production line")
    ]
    standard_dt = fields.Integer(
        string="Desired Delivery Time",
        help="Desired delivery time in working days",
        default=20,
    )
    standard_pd = fields.Date(
        string="Desired Date",
        compute="_get_standard_pd",
        help="Delivery date calculated with Desired Delivery Date",
    )
    earliest_date = fields.Date(
        compute="_get_earliest_date",
    )
    suggested_date = fields.Date(
        string="Date to promise",
        help="According to load, the latest between desired and what load allows.",
        compute="_get_suggested_date",
    )
    ccr_1 = fields.Char(
        string="CCR 1",
        default="CCR 1 name",
    )
    ccr_2 = fields.Char(
        string="CCR 2",
        default="CCR 2 name",
    )
    ccr_3 = fields.Char(
        string="CCR 3",
        default="CCR 3 name",
    )
    hours_day_1 = fields.Float(
        string="Hours per working day CCR 1",
        default=8.0,
    )
    reserved_mto_1 = fields.Float(
        string="Cap % for MTO",
        default=100,
    )
    hours_day_2 = fields.Float(
        string="Hours per working day CCR 2",
        default=8.0,
    )
    reserved_mto_2 = fields.Float(
        string="Cap % for MTO",
        default=100,
    )
    hours_day_3 = fields.Float(
        string="Hours per working day CCR 3",
        default=8.0,
    )
    reserved_mto_3 = fields.Float(
        string="Cap % for MTO",
        default=100,
    )
    load_front_1 = fields.Float(
        string="Load MTO",
        help="Percentage of used capacity in target WIP time",
        compute="_get_load_front_1",
    )
    load_front_2 = fields.Float(
        string="Load MTO",
        help="Percentage of used reserved capacity in target WIP time",
        compute="_get_load_front_2",
    )
    load_front_3 = fields.Float(
        string="Load MTO",
        help="Percentage of used reserved capacity in target WIP time",
        compute="_get_load_front_3",
    )
    load_mta_1 = fields.Float(
        string="Load MTA",
        help="Percentage of used reserved capacity in target WIP time",
        compute="_get_load_mta_1",
    )
    load_mta_2 = fields.Float(
        string="Load MTA",
        help="Percentage of used reserved capacity in target WIP time",
        compute="_get_load_mta_2",
    )
    load_mta_3 = fields.Float(
        string="Load MTA",
        help="Percentage of used reserved capacity in target WIP time",
        compute="_get_load_mta_3",
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
        help="A healthy WIP in days for this line, around 50%-80% of average buffer",
        default=5,
    )
    total_days_1 = fields.Float(
        string="Future MTO load",
        help="Total committed load in days",
        compute="_get_total_days_1",
    )
    total_days_2 = fields.Float(
        string="Future MTO load",
        help="Total committed load in days",
        compute="_get_total_days_2",
    )
    total_days_3 = fields.Float(
        string="Future MTO load",
        help="Total committed load in days",
        compute="_get_total_days_3",
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

    @api.depends("min_buffer", "hours_day_1", "reserved_mto_1")
    def _get_load_front_1(self):
        self.load_front_1 = 0
        capacity_reserved = self.min_buffer * \
            self.hours_day_1 * self.reserved_mto_1 / 100
        if capacity_reserved > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name),
                 ('order_type', '=', 'MTO')],
                ['hours_ccr_1'])
            hrs_wos = [i['hours_ccr_1'] for i in w_orders]
            hours_ccr = 0
            for hr_wo in hrs_wos:
                hours_ccr = hours_ccr + hr_wo
            self.load_front_1 = 100 * hours_ccr / capacity_reserved

    @api.depends("min_buffer", "hours_day_2", "reserved_mto_2")
    def _get_load_front_2(self):
        self.load_front_2 = 0
        capacity_reserved = self.min_buffer * \
            self.hours_day_2 * self.reserved_mto_2 / 100
        if capacity_reserved > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name),
                 ('order_type', '=', 'MTO')],
                ['hours_ccr_2'])
            hrs_wos = [i['hours_ccr_2'] for i in w_orders]
            hours_ccr = 0
            for hr_wo in hrs_wos:
                hours_ccr = hours_ccr + hr_wo
            self.load_front_2 = 100 * hours_ccr / capacity_reserved

    @api.depends("min_buffer", "hours_day_3", "reserved_mto_3")
    def _get_load_front_3(self):
        self.load_front_3 = 0
        capacity_reserved = self.min_buffer * \
            self.hours_day_3 * self.reserved_mto_3 / 100
        if capacity_reserved > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name),
                 ('order_type', '=', 'MTO')],
                ['hours_ccr_3'])
            hrs_wos = [i['hours_ccr_3'] for i in w_orders]
            hours_ccr = 0
            for hr_wo in hrs_wos:
                hours_ccr = hours_ccr + hr_wo
            self.load_front_3 = 100 * hours_ccr / capacity_reserved

    @api.depends("min_buffer", "hours_day_1", "reserved_mto_1")
    def _get_load_mta_1(self):
        self.load_mta_1 = 0
        capacity_reserved = self.min_buffer * \
            self.hours_day_1 * (1 - self.reserved_mto_1 / 100)
        if capacity_reserved > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name),
                 ('order_type', '=', 'MTA')],
                ['total_hours_ccr_1'])
            hrs_wos = [i['total_hours_ccr_1'] for i in w_orders]
            hours_ccr = 0
            for hr_wo in hrs_wos:
                hours_ccr = hours_ccr + hr_wo
            self.load_mta_1 = 100 * hours_ccr / capacity_reserved

    @api.depends("min_buffer", "hours_day_2", "reserved_mto_2")
    def _get_load_mta_2(self):
        self.load_mta_2 = 0
        capacity_reserved = self.min_buffer * \
            self.hours_day_2 * (1 - self.reserved_mto_2 / 100)
        if capacity_reserved > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name),
                 ('order_type', '=', 'MTA')],
                ['total_hours_ccr_2'])
            hrs_wos = [i['total_hours_ccr_2'] for i in w_orders]
            hours_ccr = 0
            for hr_wo in hrs_wos:
                hours_ccr = hours_ccr + hr_wo
            self.load_mta_2 = 100 * hours_ccr / capacity_reserved

    @api.depends("min_buffer", "hours_day_3", "reserved_mto_3")
    def _get_load_mta_3(self):
        self.load_mta_3 = 0
        capacity_reserved = self.min_buffer * \
            self.hours_day_3 * (1 - self.reserved_mto_3 / 100)
        if capacity_reserved > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name),
                 ('order_type', '=', 'MTA')],
                ['total_hours_ccr_3'])
            hrs_wos = [i['total_hours_ccr_3'] for i in w_orders]
            hours_ccr = 0
            for hr_wo in hrs_wos:
                hours_ccr = hours_ccr + hr_wo
            self.load_mta_3 = 100 * hours_ccr / capacity_reserved

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

    @api.depends("hours_day_1", "reserved_mto_1")
    def _get_total_days_1(self):
        self.total_days_1 = 0
        hours_per_day = self.hours_day_1 * self.reserved_mto_1 / 100
        if hours_per_day > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name),
                 ('order_type', '=', 'MTO')],
                ['total_hours_ccr_1'])
            total_hrs_wos = [i['total_hours_ccr_1'] for i in w_orders]
            total_hours_ccr = 0
            for tot_hrs in total_hrs_wos:
                total_hours_ccr = total_hours_ccr + tot_hrs
            self.total_days_1 = total_hours_ccr / hours_per_day

    @api.depends("hours_day_2", "reserved_mto_2")
    def _get_total_days_2(self):
        self.total_days_2 = 0
        hours_per_day = self.hours_day_2 * self.reserved_mto_2 / 100
        if hours_per_day > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name),
                 ('order_type', '=', 'MTO')],
                ['total_hours_ccr_2'])
            total_hrs_wos = [i['total_hours_ccr_2'] for i in w_orders]
            total_hours_ccr = 0
            for tot_hrs in total_hrs_wos:
                total_hours_ccr = total_hours_ccr + tot_hrs
            self.total_days_2 = total_hours_ccr / hours_per_day

    @api.depends("hours_day_3", "reserved_mto_3")
    def _get_total_days_3(self):
        self.total_days_3 = 0
        hours_per_day = self.hours_day_3 * self.reserved_mto_3 / 100
        if hours_per_day > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name),
                 ('order_type', '=', 'MTO')],
                ['total_hours_ccr_3'])
            total_hrs_wos = [i['total_hours_ccr_3'] for i in w_orders]
            total_hours_ccr = 0
            for tot_hrs in total_hrs_wos:
                total_hours_ccr = total_hours_ccr + tot_hrs
            self.total_days_3 = total_hours_ccr / hours_per_day

    @api.depends("hours_day_1", "hours_day_2", "hours_day_3",
                 "reserved_mto_1", "reserved_mto_2", "reserved_mto_3",
                 "min_buffer")
    def _get_earliest_date(self):
        today = fields.Date.today()
        self.earliest_date = today
        hpd1 = self.hours_day_1 * self.reserved_mto_1 / 100
        hpd2 = self.hours_day_2 * self.reserved_mto_2 / 100
        hpd3 = self.hours_day_3 * self.reserved_mto_3 / 100
        company_domain = [('company_id', '=', self.env.user.parent_id.name),
                          ('order_type', '=', 'MTO')]
        wo_model = self.env["otif100.work_order"].search(company_domain)
        tot_hrs = [[r.due_date, r.total_hours_ccr_1,
                    r.total_hours_ccr_2, r.total_hours_ccr_3] for r in wo_model]
        tot_hrs = sorted(tot_hrs, key=lambda x: x[0])
        wds1, wds2, wds3 = 0, 0, 0
        for r in tot_hrs:
            if hpd1 > 0:
                wds1 = wds1 + r[1] / hpd1
            if hpd2 > 0:
                wds2 = wds2 + r[2] / hpd2
            if hpd3 > 0:
                wds3 = wds3 + r[3] / hpd3
            r[1], r[2], r[3] = wds1, wds2, wds3
        nw_days = self.env["otif100.nwd"].search_read(
            [('company_id', '=', self.env.user.parent_id.name)], ['nwds'])
        nw_dates = [i['nwds'] for i in nw_days]
        tot_av_wds = [[r[0], 0] for r in tot_hrs]
        for r in tot_av_wds:
            wds, cur_date = 0, today
            while cur_date < r[0]:
                if cur_date not in nw_dates:
                    wds = wds + 1
                cur_date = cur_date + timedelta(days=1)
            r[1] = wds
        pos_date = len(tot_av_wds) - 1
        while pos_date > 0:
            max_wds = tot_av_wds[pos_date][1]
            if tot_hrs[pos_date][1] > 0 and tot_hrs[pos_date][1] > max_wds:
                max_wds = tot_hrs[pos_date][1]
            if tot_hrs[pos_date][2] > 0 and tot_hrs[pos_date][2] > max_wds:
                max_wds = tot_hrs[pos_date][2]
            if tot_hrs[pos_date][3] > 0 and tot_hrs[pos_date][3] > max_wds:
                max_wds = tot_hrs[pos_date][3]
            if tot_av_wds[pos_date][1] < max_wds:
                break
            pos_date = pos_date - 1
        if pos_date >= 0 and tot_av_wds[pos_date][0] > today:
            # 1/2 target WIP más de seguridad - parecido a FL+PB/2
            ext_wds = max_wds - \
                tot_av_wds[pos_date][1] + int(self.min_buffer / 2)
            cur_date = tot_av_wds[pos_date][0]
            while ext_wds >= 0:
                if cur_date not in nw_dates:
                    ext_wds = ext_wds - 1
                cur_date = cur_date + timedelta(days=1)
            self.earliest_date = cur_date

    @api.depends("earliest_date", "standard_pd")
    def _get_suggested_date(self):
        if self.standard_pd > self.earliest_date:
            self.suggested_date = self.standard_pd
        else:
            self.suggested_date = self.earliest_date
