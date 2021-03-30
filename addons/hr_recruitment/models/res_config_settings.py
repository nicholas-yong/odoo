# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    module_website_hr_recruitment = fields.Boolean(string='Online Posting')
    module_hr_recruitment_survey = fields.Boolean(string='Interview Forms')
    module_hr_recruitment_autoSendEmail = fields.Boolean(string='Automatically Send Email?')

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('module_hr_recruitment_autoSendEmail', self.module_hr_recruitment_autoSendEmail )
        return res
    
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        sudo = self.env['ir.config_parameter'].sudo()
        default_recruitment_send_email = sudo.get_param('module_hr_recruitment_autoSendEmail')
        res.update( module_hr_recruitment_autoSendEmail = default_recruitment_send_email )
        return res;
