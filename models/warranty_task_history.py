# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2018-Today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from odoo import api, fields, models, _

class WarrantyTaskHistory(models.Model):
    _name = "warranty.task.history"
    _rec_name = "warranty_id"

    warranty_id = fields.Many2one('warranty.details', string='Order')
    warranty_task_id = fields.Many2one('warranty.task', string='Warranty Task')
    done = fields.Boolean(string = 'Task Done', default = False)

    @api.depends('warranty_task_id')
    def warranty_checklist_progress(self):
		for rec in self:
			total_len = self.env['warranty.task'].search_count([])
			check_list_len = len(rec.warranty_task_id)
			if total_len != 0:
				rec.warranty_checklist_progress = (check_list_len*100) / total_len

    warranty_task_id = fields.Many2many('warranty.task', string='Check List')
    warranty_checklist_progress = fields.Float(compute=warranty_checklist_progress, string='Progress', store=True, recompute=True,
                                      default=0.0)
    max_rate = fields.Integer(string='Maximum rate', default=100)







