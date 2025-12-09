from odoo import models, fields, api
from odoo.addons.xyz.tools.misc import decrypt_bytes
from odoo.addons.integration_xero.models.xero import XERO_AUTH_URL
from urllib.parse import urlencode

class ResUsers(models.Model):
    _inherit = "res.users"

    xero_access_token = fields.Char('Xero Access Token', exportable=False, readonly=True)
    xero_refresh_token = fields.Char('Xero Refresh Token', exportable=False, readonly=True)
    xero_refresh_token_decrypted = fields.Char('Xero Refresh Token (Decrypted)', compute='_compute_xero_refresh_token_decrypted')

    @api.model
    def action_get(self):
        action = self.sudo().env.ref('mail.action_res_users_my_fullpage').read()[0]
        action['target'] = 'main'
        return action

    @api.depends('xero_refresh_token')
    def _compute_xero_refresh_token_decrypted(self):
        for record in self:
            record.xero_refresh_token_decrypted = decrypt_bytes(self.xero_refresh_token)

    def preference_xero_connect(self):
        provider = self.env.ref('integration_xero.integration_integration_xero')

        xero_params = {
            "response_type": "code",
            "client_id": provider.client_id,
            "redirect_uri": provider.redirect_uri,
            "scope": "openid profile email accounting.transactions",
            "state": "connect",
        }
        url = f"{XERO_AUTH_URL}?{urlencode(xero_params)}"
        return {
            'type': 'ir.actions.client',
            'tag': 'xero_integration.oauth',
            'params': {
                'url': url
            }
        }