from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    jwt_algorithm = fields.Selection(related="company_id.jwt_algorithm")
    jwt_access_token_duration = fields.Integer(related="company_id.jwt_access_token_duration", readonly=False)
    jwt_refresh_token_duration = fields.Integer(related="company_id.jwt_refresh_token_duration", readonly=False)