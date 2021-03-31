# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ApplicantGetRefuseReason(models.TransientModel):
    _name = 'applicant.get.refuse.reason'
    _description = 'Get Refuse Reason'

    refuse_reason_id = fields.Many2one('hr.applicant.refuse.reason', 'Refuse Reason')
    applicant_ids = fields.Many2many('hr.applicant')
    send_email = fields.Boolean('Send Email?', default=True)
    #template_id = fields.Many2one('mail.template', string="Mail Template", 

    def action_refuse_reason_apply(self):
        if self.send_email:
            template = self.env['mail.template'].search([('name', '=', 'Applicant: Refuse')])
            self.applicant_ids.env['mail.template'].browse(template.id).send_mail(self.applicant_ids.id, force_send=True )
            
        return self.applicant_ids.write({'refuse_reason_id': self.refuse_reason_id.id, 'active': False})
