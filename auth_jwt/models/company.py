from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    jwt_algorithm = fields.Selection([('HS256', 'HS256')], string="JWT Algorithm", default='HS256', required=True)
    jwt_access_token_duration = fields.Integer(string="JWT Access Token Duration", default=60)
    jwt_refresh_token_duration = fields.Integer(string="JWT Refresh Token Duration", default=3600)