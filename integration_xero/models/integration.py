from odoo import models, fields

class Ingetration(models.Model):
    _inherit = 'integration.integration'

    provider = fields.Selection(selection_add=[('xero', 'Xero')], ondelete={'xero': 'set default'})