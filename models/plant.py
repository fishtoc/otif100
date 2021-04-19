from odoo import models, fields, api, exceptions
from datetime import timedelta


class Plant(models.Model):
    _name = 'otif100.plant'

    name = fields.Char(
        string="Plant name",
        default="My plant name",
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
    suggested_date = fields.Date(
        string="Date to promise according to selected CCRs",
        help="The earliest possible date according to load on selected CCRs",
        compute="_get_suggested_date",
    )
    earliest_date = fields.Date(
        string="Date to promise",
        help="The earliest according to load",
        compute="_get_earliest_date",
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
    ccr_4 = fields.Char(
        string="CCR 4",
        default="CCR 4 name",
    )
    ccr_5 = fields.Char(
        string="CCR 5",
        default="CCR 5 name",
    )
    ccr_6 = fields.Char(
        string="CCR 6",
        default="CCR 6 name",
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
    hours_day_4 = fields.Float(
        string="Hours per working day CCR 4",
        default=8.0,
    )
    hours_day_5 = fields.Float(
        string="Hours per working day CCR 5",
        default=8.0,
    )
    hours_day_6 = fields.Float(
        string="Hours per working day CCR 6",
        default=8.0,
    )
    reserved_mto_1 = fields.Float(
        string="Cap % for MTO",
        default=100,
    )
    reserved_mto_2 = fields.Float(
        string="Cap % for MTO",
        default=100,
    )
    reserved_mto_3 = fields.Float(
        string="Cap % for MTO",
        default=100,
    )
    reserved_mto_4 = fields.Float(
        string="Cap % for MTO",
        default=100,
    )
    reserved_mto_5 = fields.Float(
        string="Cap % for MTO",
        default=100,
    )
    reserved_mto_6 = fields.Float(
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
    load_front_4 = fields.Float(
        string="Load MTO",
        help="Percentage of used reserved capacity in target WIP time",
        compute="_get_load_front_4",
    )
    load_front_5 = fields.Float(
        string="Load MTO",
        help="Percentage of used reserved capacity in target WIP time",
        compute="_get_load_front_5",
    )
    load_front_6 = fields.Float(
        string="Load MTO",
        help="Percentage of used reserved capacity in target WIP time",
        compute="_get_load_front_6",
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
    load_mta_4 = fields.Float(
        string="Load MTA",
        help="Percentage of used reserved capacity in target WIP time",
        compute="_get_load_mta_4",
    )
    load_mta_5 = fields.Float(
        string="Load MTA",
        help="Percentage of used reserved capacity in target WIP time",
        compute="_get_load_mta_5",
    )
    load_mta_6 = fields.Float(
        string="Load MTA",
        help="Percentage of used reserved capacity in target WIP time",
        compute="_get_load_mta_6",
    )
    avg_buffer_1 = fields.Integer(
        string="Target WIP in working days",
        help="A healthy WIP in days for this CCR, around 50%-80% of average buffer for products going throug it",
        default=7,
    )
    avg_buffer_2 = fields.Integer(
        string="Target WIP in working days",
        help="A healthy WIP in days for this CCR, around 50%-80% of average buffer for products going throug it",
        default=7,
    )
    avg_buffer_3 = fields.Integer(
        string="Target WIP in working days",
        help="A healthy WIP in days for this CCR, around 50%-80% of average buffer for products going throug it",
        default=7,
    )
    avg_buffer_4 = fields.Integer(
        string="Target WIP in working days",
        help="A healthy WIP in days for this CCR, around 50%-80% of average buffer for products going throug it",
        default=7,
    )
    avg_buffer_5 = fields.Integer(
        string="Target WIP in working days",
        help="A healthy WIP in days for this CCR, around 50%-80% of average buffer for products going throug it",
        default=7,
    )
    avg_buffer_6 = fields.Integer(
        string="Target WIP in working days",
        help="A healthy WIP in days for this CCR, around 50%-80% of average buffer for products going throug it",
        default=7,
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
    total_days_4 = fields.Float(
        string="Future MTO load",
        help="Total committed load in days",
        compute="_get_total_days_4",
    )
    total_days_5 = fields.Float(
        string="Future MTO load",
        help="Total committed load in days",
        compute="_get_total_days_5",
    )
    total_days_6 = fields.Float(
        string="Future MTO load",
        help="Total committed load in days",
        compute="_get_total_days_6",
    )
    edd_1 = fields.Date(
        string="Earliest date to promise",
        help="This is the earliest date to promise for products going through this CCR",
        compute="_get_edd_1",
    )
    edd_2 = fields.Date(
        string="Earliest date to promise",
        help="This is the earliest date to promise for products going through this CCR",
        compute="_get_edd_2",
    )
    edd_3 = fields.Date(
        string="Earliest date to promise",
        help="This is the earliest date to promise for products going through this CCR",
        compute="_get_edd_3",
    )
    edd_4 = fields.Date(
        string="Earliest date to promise",
        help="This is the earliest date to promise for products going through this CCR",
        compute="_get_edd_4",
    )
    edd_5 = fields.Date(
        string="Earliest date to promise",
        help="This is the earliest date to promise for products going through this CCR",
        compute="_get_edd_5",
    )
    edd_6 = fields.Date(
        string="Earliest date to promise",
        help="This is the earliest date to promise for products going through this CCR",
        compute="_get_edd_6",
    )
    ccr1_included = fields.Boolean(
        string="Include CCR1",
        default=True,
        help="Mark it if the SKU to be quoted is processed by this CCR",
    )    
    ccr2_included = fields.Boolean(
        string="Include CCR2",
        default=True,
        help="Mark it if the SKU to be quoted is processed by this CCR",
    )
    ccr3_included = fields.Boolean(
        string="Include CCR3",
        default=True,
        help="Mark it if the SKU to be quoted is processed by this CCR",
    )
    ccr4_included = fields.Boolean(
        string="Include CCR4",
        default=True,
        help="Mark it if the SKU to be quoted is processed by this CCR",
    )
    ccr5_included = fields.Boolean(
        string="Include CCR5",
        default=True,
        help="Mark it if the SKU to be quoted is processed by this CCR",
    )
    ccr6_included = fields.Boolean(
        string="Include CCR6",
        default=True,
        help="Mark it if the SKU to be quoted is processed by this CCR",
    )

    # Función genérica para calcular frente de carga MTO
    def get_load_front_x(self, avg_buffer, hours_day, reserved_mto, hrs_ccr):
        load_front_1 = 0
        capacity_reserved = avg_buffer * hours_day * reserved_mto / 100
        if capacity_reserved > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name),
                 ('order_type', '=', 'MTO')],
                [hrs_ccr])
            hrs_wos = [i[hrs_ccr] for i in w_orders]
            hours_ccr = 0
            for hr_wo in hrs_wos:
                hours_ccr = hours_ccr + hr_wo
            load_front_1 = 100 * hours_ccr / capacity_reserved
        return load_front_1

    @api.depends("avg_buffer_1", "hours_day_1", "reserved_mto_1")
    def _get_load_front_1(self):
        self.load_front_1 = self.get_load_front_x(
            self.avg_buffer_1,
            self.hours_day_1,
            self.reserved_mto_1,
            'hours_ccr_1'
        )

    @api.depends("avg_buffer_2", "hours_day_2", "reserved_mto_2")
    def _get_load_front_2(self):
        self.load_front_2 = self.get_load_front_x(
            self.avg_buffer_2,
            self.hours_day_2,
            self.reserved_mto_2,
            'hours_ccr_2'
        )

    @api.depends("avg_buffer_3", "hours_day_3", "reserved_mto_3")
    def _get_load_front_3(self):
        self.load_front_3 = self.get_load_front_x(
            self.avg_buffer_3,
            self.hours_day_3,
            self.reserved_mto_3,
            'hours_ccr_3'
        )

    @api.depends("avg_buffer_4", "hours_day_4", "reserved_mto_4")
    def _get_load_front_4(self):
        self.load_front_4 = self.get_load_front_x(
            self.avg_buffer_4,
            self.hours_day_4,
            self.reserved_mto_4,
            'hours_ccr_4'
        )

    @api.depends("avg_buffer_5", "hours_day_5", "reserved_mto_5")
    def _get_load_front_5(self):
        self.load_front_5 = self.get_load_front_x(
            self.avg_buffer_5,
            self.hours_day_5,
            self.reserved_mto_5,
            'hours_ccr_5'
        )

    @api.depends("avg_buffer_6", "hours_day_6", "reserved_mto_6")
    def _get_load_front_6(self):
        self.load_front_6 = self.get_load_front_x(
            self.avg_buffer_6,
            self.hours_day_6,
            self.reserved_mto_6,
            'hours_ccr_6'
        )

    # Calcula carga MTA genérica
    def get_load_mta_x(self, avg_buffer, hours_day, reserved_mto, tot_hrs_ccr ):
        load_mta = 0
        capacity_reserved = avg_buffer * hours_day * (1 - reserved_mto / 100)
        if capacity_reserved > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name),
                 ('order_type', '=', 'MTA')],
                [tot_hrs_ccr])
            hrs_wos = [i[tot_hrs_ccr] for i in w_orders]
            hours_ccr = 0
            for hr_wo in hrs_wos:
                hours_ccr = hours_ccr + hr_wo
            load_mta = 100 * hours_ccr / capacity_reserved
        return load_mta

    @api.depends("avg_buffer_1", "hours_day_1", "reserved_mto_1")
    def _get_load_mta_1(self):
        self.load_mta_1 = self.get_load_mta_x(
            self.avg_buffer_1,
            self.hours_day_1,
            self.reserved_mto_1,
            'total_hours_ccr_1'
        )
 
    @api.depends("avg_buffer_2", "hours_day_2", "reserved_mto_2")
    def _get_load_mta_2(self):
        self.load_mta_2 = self.get_load_mta_x(
            self.avg_buffer_2,
            self.hours_day_2,
            self.reserved_mto_2,
            'total_hours_ccr_2'
        )

    @api.depends("avg_buffer_3", "hours_day_3", "reserved_mto_3")
    def _get_load_mta_3(self):
        self.load_mta_3 = self.get_load_mta_x(
            self.avg_buffer_3,
            self.hours_day_3,
            self.reserved_mto_3,
            'total_hours_ccr_3'
        )

    @api.depends("avg_buffer_4", "hours_day_4", "reserved_mto_4")
    def _get_load_mta_4(self):
        self.load_mta_4 = self.get_load_mta_x(
            self.avg_buffer_4,
            self.hours_day_4,
            self.reserved_mto_4,
            'total_hours_ccr_4'
        )

    @api.depends("avg_buffer_5", "hours_day_5", "reserved_mto_5")
    def _get_load_mta_5(self):
        self.load_mta_5 = self.get_load_mta_x(
            self.avg_buffer_5,
            self.hours_day_5,
            self.reserved_mto_5,
            'total_hours_ccr_5'
        )

    @api.depends("avg_buffer_6", "hours_day_6", "reserved_mto_6")
    def _get_load_mta_6(self):
        self.load_mta_6 = self.get_load_mta_x(
            self.avg_buffer_6,
            self.hours_day_6,
            self.reserved_mto_6,
            'total_hours_ccr_6'
        )

    # Calcula días totales genérico
    def get_total_days_x(self, hours_day, reserved_mto, tot_hrs_ccr):
        total_days = 0
        hours_per_day = hours_day * reserved_mto / 100
        if hours_per_day > 0:
            w_orders = self.env["otif100.work_order"].search_read(
                [('company_id', '=', self.env.user.parent_id.name),
                 ('order_type', '=', 'MTO')],
                [tot_hrs_ccr])
            total_hrs_wos = [i[tot_hrs_ccr] for i in w_orders]
            total_hours_ccr = 0
            for tot_hrs in total_hrs_wos:
                total_hours_ccr = total_hours_ccr + tot_hrs
            total_days = total_hours_ccr / hours_per_day
        return total_days


    @api.depends("hours_day_1", "reserved_mto_1")
    def _get_total_days_1(self):
        self.total_days_1 = self.get_total_days_x(
            self.hours_day_1,
            self.reserved_mto_1,
            'total_hours_ccr_1'
        )

    @api.depends("hours_day_2", "reserved_mto_2")
    def _get_total_days_2(self):
        self.total_days_2 = self.get_total_days_x(
            self.hours_day_2,
            self.reserved_mto_2,
            'total_hours_ccr_2'
        )

    @api.depends("hours_day_3", "reserved_mto_3")
    def _get_total_days_3(self):
        self.total_days_3 = self.get_total_days_x(
            self.hours_day_3,
            self.reserved_mto_3,
            'total_hours_ccr_3'
        )

    @api.depends("hours_day_4", "reserved_mto_4")
    def _get_total_days_4(self):
        self.total_days_4 = self.get_total_days_x(
            self.hours_day_4,
            self.reserved_mto_4,
            'total_hours_ccr_4'
        )

    @api.depends("hours_day_5", "reserved_mto_5")
    def _get_total_days_5(self):
        self.total_days_5 = self.get_total_days_x(
            self.hours_day_5,
            self.reserved_mto_5,
            'total_hours_ccr_5'
        )

    @api.depends("hours_day_6", "reserved_mto_6")
    def _get_total_days_6(self):
        self.total_days_6 = self.get_total_days_x(
            self.hours_day_6,
            self.reserved_mto_6,
            'total_hours_ccr_6'
        )

    # Calcula la fecha más temrana en CCR genérico
    def get_earliest_date_x(self, avg_buffer, hours_day, reserved_mto, total_hours_field):
        today = fields.Date.today()
        earliest_day = today # Inicializa la variable
        # Agrega 80% del WIP objetivo como amortiguador
        half_pb = int(avg_buffer * 0.80)
        # Calcula hpd horas por día
        hpd = hours_day * reserved_mto / 100
        # Obtiene recordset con todas las órdenes MTO
        company_domain = [('company_id', '=', self.env.user.parent_id.name),
                          ('order_type', '=', 'MTO')]
        wo_model = self.env["otif100.work_order"].search(company_domain)
        # Recorre la lista de diccionarios wo_model y construye lista de pares [fecha_ent, hrs_ccr]
        tot_hrs = [[r["due_date"], r[total_hours_field]] for r in wo_model]
        # Ordena la nueva lista por fecha ascendente
        tot_hrs = sorted(tot_hrs, key=lambda x: x[0])
        # Sustituye horas por días hábiles acumulados en el par
        wds = 0
        for r in tot_hrs:
            if hpd > 0:
                wds += r[1] / hpd
            r[1] = wds # Lo eran horas, ahora son días hábiles acumulados (working days)
    
        #Obtiene recordset de días no hábiles
        nw_days = self.env["otif100.nwd"].search_read(
            [('company_id', '=', self.env.user.parent_id.name)], ['nwds'])
        # Construye la lista nw_dates con los días no hábiles, sin descripciones
        nw_dates = [i['nwds'] for i in nw_days]
        #
        #Teniendo la lista de pares ordenada en orden ascendente, buscamos la fecha más tardía
        last_pos = len(tot_hrs) - 1
        last_date = tot_hrs[last_pos][0]
        # Construye lista de pares [fecha_habil, wd_acc]
        tot_wds = []
        # Encuentre primer día hábil cerca de hoy
        first_day = today
        while first_day in nw_dates:
            first_day -= timedelta(days=1) # Retrocede un día
        # inicia lista de pares con el primero con 1 día hábil acumulado
        tot_wds.append([first_day, 1]) # empezamos en primer día  
        # Construye lista hasta el último día de tot_hrs
        next_wd = first_day + timedelta(days=1)
        while next_wd in nw_dates:
            next_wd += timedelta(days=1)
        tot_wds.append([next_wd, 2])
        wd_acc = 3
        while next_wd <= last_date:
            next_wd += timedelta(days=1) # busca siguiente
            if next_wd not in nw_dates:
                tot_wds.append([next_wd,wd_acc])
                wd_acc += 1
        # Construye diccionario [fecha_habil: xxx, wd_acc: correlativo]
        claves = [i[0] for i in tot_wds]
        valores = [i[1] for i in tot_wds]
        working_days = dict(zip(claves,valores))
        # Finalmente, en tot_hrs busca la primera fecha donde días comprometidos acumulados
        # es menor que días acumulados, recorriendo desde la última hacia atrás
        pos = max(0,len(tot_hrs) - 1)
        cur_date = tot_hrs[pos][0]
        while pos > 0 and cur_date > today:
            cur_date = tot_hrs[pos][0]      # fecha en el par
            if cur_date not in nw_dates:    # puede haber fechas prometidas en día no hábil
                if tot_hrs[pos][1] > working_days[cur_date]:
                    cur_date += timedelta(days=1) # el día siguiente al que cumplió condición
                    break                         # sale del loop        
            pos -= 1
        # cur_date tiene el frente de carga, ahora sumamos medio amortiguador half_pb
        earliest_date = cur_date
        i = half_pb
        while i > 0:
            earliest_date += timedelta(days=1)
            if earliest_date not in nw_dates:
                i -= 1
        return earliest_date

    @api.depends("hours_day_1", "reserved_mto_1")
    def _get_edd_1(self):
        self.edd_1 = self.get_earliest_date_x(
            self.avg_buffer_1,
            self.hours_day_1,
            self.reserved_mto_1,
            'total_hours_ccr_1'
        )

    @api.depends("hours_day_2", "reserved_mto_2")
    def _get_edd_2(self):
        self.edd_2 = self.get_earliest_date_x(
            self.avg_buffer_2,
            self.hours_day_2,
            self.reserved_mto_2,
            'total_hours_ccr_2'
        )

    @api.depends("hours_day_3", "reserved_mto_3")
    def _get_edd_3(self):
        self.edd_3 = self.get_earliest_date_x(
            self.avg_buffer_3,
            self.hours_day_3,
            self.reserved_mto_3,
            'total_hours_ccr_3'
        )

    @api.depends("hours_day_4", "reserved_mto_4")
    def _get_edd_4(self):
        self.edd_4 = self.get_earliest_date_x(
            self.avg_buffer_4,
            self.hours_day_4,
            self.reserved_mto_4,
            'total_hours_ccr_4'
        )

    @api.depends("hours_day_5", "reserved_mto_5")
    def _get_edd_5(self):
        self.edd_5 = self.get_earliest_date_x(
            self.avg_buffer_5,
            self.hours_day_5,
            self.reserved_mto_5,
            'total_hours_ccr_5'
        )

    @api.depends("hours_day_6", "reserved_mto_6")
    def _get_edd_6(self):
        self.edd_6 = self.get_earliest_date_x(
            self.avg_buffer_6,
            self.hours_day_6,
            self.reserved_mto_6,
            'total_hours_ccr_6'
        )

    @api.depends("ccr1_included", "ccr2_included", "ccr3_included",
                 "ccr4_included", "ccr5_included", "ccr6_included",
                 "edd_1", "edd_2", "edd_3", "edd_4", "edd_5", "edd_6")
    def _get_earliest_date(self):
        edd = fields.Date.today()
        try:
            if self.ccr1_included:
                edd = max(edd, self.edd_1)
            if self.ccr2_included:
                edd = max(edd, self.edd_2)
            if self.ccr3_included:
                edd = max(edd, self.edd_3)
            if self.ccr4_included:
                edd = max(edd, self.edd_4)
            if self.ccr5_included:
                edd = max(edd, self.edd_5)
            if self.ccr6_included:
                edd = max(edd, self.edd_6)
        except:
            pass
        self.earliest_date = edd
            
    @api.depends("earliest_date")
    def _get_suggested_date(self):
        self.suggested_date = self.earliest_date

