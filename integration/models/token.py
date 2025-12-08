from odoo import models, fields

class JWTRefreshToken(models.Model):
    _inherit = 'res.users.jwt.refresh'

    integration_application_id = fields.Many2one("integration.application", "Application", ondelete="cascade")