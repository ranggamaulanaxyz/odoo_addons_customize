from odoo import models, fields, api
from odoo.addons.xyz.tools.misc import decrypt_bytes

class ResUsers(models.Model):
    _inherit = "res.users"

    xero_access_token = fields.Char('Xero Access Token', exportable=False, readonly=True)
    xero_refresh_token = fields.Char('Xero Refresh Token', exportable=False, readonly=True)
    xero_refresh_token_decrypted = fields.Char('Xero Refresh Token (Decrypted)', compute='_compute_xero_refresh_token_decrypted')

    @api.depends('xero_refresh_token')
    def _compute_xero_refresh_token_decrypted(self):
        for record in self:
            record.xero_refresh_token_decrypted = decrypt_bytes(self.xero_refresh_token)

    def preference_xero_connect(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'xero_integration.oauth',
            'params': {}
        }