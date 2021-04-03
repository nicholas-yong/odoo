# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError


class HrPlanWizard(models.TransientModel):
    _name = 'hr.plan.wizard'
    _description = 'Plan Wizard'

    employee_id = fields.Many2one(
        'hr.employee', string='Employee', required=True,
        default=lambda self: self.env.context.get('active_id', None),
    )
    plan_id = fields.Many2one('hr.plan')
    employee_id_staff_type = fields.Char(string='Employee Staff Type', compute = "_get_staff_type")
    is_button_visible = fields.Boolean(string="Can Proceed with Launching Action", compute ="_get_button_visible")

    @api.depends('plan_id')
    def _get_button_visible(self):
        self.is_button_visible = self.plan_id.id != False

    @api.depends('employee_id')
    def _get_staff_type(self):
        self.employee_id_staff_type = self.employee_id.staff_type

    @api.depends('employee_id')
    def _get_plan_id(self):
        employee_staff_type = self.employee_id.staff_type
        plans = self.env['hr.plan'].search([('staff_type', '=', employee_staff_type)])
        self.plan_id = plans

    def action_launch(self):
        for activity_type in self.plan_id.plan_activity_type_ids:
            responsible = activity_type.get_responsible_id(self.employee_id)

            if self.env['hr.employee'].with_user(responsible).check_access_rights('read', raise_exception=False):
                date_deadline = self.env['mail.activity']._calculate_date_deadline(activity_type.activity_type_id)
                self.employee_id.activity_schedule(
                    activity_type_id=activity_type.activity_type_id.id,
                    summary=activity_type.summary,
                    note=activity_type.note,
                    user_id=responsible.id,
                    date_deadline=date_deadline
                )

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.employee',
            'res_id': self.employee_id.id,
            'name': self.employee_id.display_name,
            'view_mode': 'form',
            'views': [(False, "form")],
        }
