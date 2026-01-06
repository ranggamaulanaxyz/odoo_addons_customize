from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    jwt_algorithm = fields.Selection([('HS256', 'HS256')], string="JWT Algorithm", default='HS256', required=True)
    # Duration in seconds: 900 = 15 minutes for access tokens
    jwt_access_token_duration = fields.Integer(string="JWT Access Token Duration (seconds)", default=900, help="Access token lifetime in seconds (default: 900 = 15 minutes)")
    # Duration in seconds: 604800 = 7 days for refresh tokens
    jwt_refresh_token_duration = fields.Integer(string="JWT Refresh Token Duration (seconds)", default=604800, help="Refresh token lifetime in seconds (default: 604800 = 7 days)")