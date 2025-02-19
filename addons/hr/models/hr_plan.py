# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrPlanActivityType(models.Model):
    _name = 'hr.plan.activity.type'
    _description = 'Plan activity type'
    _rec_name = 'summary'

    activity_type_id = fields.Many2one(
        'mail.activity.type', 'Activity Type',
        default=lambda self: self.env.ref('mail.mail_activity_data_todo'),
        domain=lambda self: ['|', ('res_model_id', '=', False), ('res_model_id', '=', self.env['ir.model']._get('hr.employee').id)],
        ondelete='restrict'
    )
    summary = fields.Char('Summary', compute="_compute_default_summary", store=True, readonly=False)
    responsible = fields.Selection([
        ('coach', 'Coach'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
        ('hiring_manager', 'Hiring Manager'),
        ('other', 'Other')], default='employee', string='Responsible', required=True)
    responsible_id = fields.Many2one('res.users', 'Responsible Person', help='Specific responsible of activity if not linked to the employee.')
    note = fields.Html('Note')

    @api.depends('activity_type_id')
    def _compute_default_summary(self):
        for plan_type in self:
            if not plan_type.summary and plan_type.activity_type_id and plan_type.activity_type_id.summary:
                plan_type.summary = plan_type.activity_type_id.summary

    def get_responsible_id(self, employee):
        if self.responsible == 'coach':
            if not employee.coach_id:
                raise UserError(_('Coach of employee %s is not set.', employee.name))
            responsible = employee.coach_id.user_id
            if not responsible:
                raise UserError(_('User of coach of employee %s is not set.', employee.name))
        elif self.responsible == 'manager':
            if not employee.parent_id:
                raise UserError(_('Manager of employee %s is not set.', employee.name))
            responsible = employee.parent_id.user_id
            if not responsible:
                raise UserError(_('User of manager of employee %s is not set.', employee.name))
        elif self.responsible == 'employee':
            responsible = employee.user_id
            if not responsible:
                raise UserError(_('User linked to employee %s is required.', employee.name))
        elif self.responsible == 'hiring_manager':
            #Check to see if the Hiring Manager exists
            if not employee.hiring_manager_id:
                raise UserError(_('Hiring Manager of Employee %s is not set.', employee.name))
            responsible = employee.hiring_manager_id
        elif self.responsible == 'other':
            responsible = self.responsible_id
            if not responsible:
                raise UserError(_('No specific user given on activity %s.', self.activity_type_id.name))
        return responsible


class HrPlan(models.Model):
    _name = 'hr.plan'
    _description = 'plan'

    name = fields.Char('Name', required=True)
    plan_activity_type_ids = fields.Many2many('hr.plan.activity.type', string='Activities')
    active = fields.Boolean(default=True)
    staff_type = fields.Selection([
        ('1', 'Volunteer'),
        ('2', 'Intern'),
        ('3', 'Employee'),
        ('4', 'Contractor')], string="Staff Type", help="Please select Employement Type for HR Plan", default="1", required=True)


