# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ColorUpdate(models.TransientModel):
    _name = 'otif100.color_update'

    @api.multi
    def confirm_button(self):
        self.ensure_one()
        wo = self.env['otif100.work_order']
        wo.recalculate_colors()
        return {'type': 'ir.actions.act_window_close'}
