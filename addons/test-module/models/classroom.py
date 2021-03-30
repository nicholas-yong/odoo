# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SchoolNew( models.Model ):
    _name = 'school'
    _description = 'A Model representing a school.'

    name = fields.Char( 'Description', required = True )
    roll_number = fields.Integer( 'Roll Number', required = True )
    division = fields.Char( 'Div' )