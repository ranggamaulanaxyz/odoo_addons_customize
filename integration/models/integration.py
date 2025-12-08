from odoo import models, fields

class Integration(models.Model):
    _name = 'integration.integration'
    _description = 'Integration'

    provider = fields.Selection([('manual', 'Manual')], string='Provider', default='manual', required=True, copy=False)