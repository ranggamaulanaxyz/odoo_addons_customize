import logging
from odoo import models, fields, _
from odoo.exceptions import AccessError, AccessDenied
from hashlib import sha256

_logger = logging.getLogger(__name__)

DEFAULT_JWT_SECRET_KEY = 'Hk5U4qM6xWgb_YzmlfJYq7hF8nGZ1E0qzDbN6oL0x5Q'

class JWTRefreshToken(models.Model):
    _name = 'res.users.jwt.refresh'
    _description = 'JWT Refresh Token'
    _rec_name = 'hash_token_id'

    hash_token_id = fields.Char(required=True)
    revoked = fields.Boolean(indexed=True)
    user_id = fields.Many2one('res.users', required=True, ondelete="cascade")

    def _hash_token_id(self, token_id):
        return sha256(token_id.encode()).hexdigest()

    def _browse_token(self, user_id, token_id):
        if not token_id:
            return self
        hash_token_id = self._hash_token_id(token_id)
        refresh_token = self.search([('hash_token_id', '=', hash_token_id)], limit=1)
        if refresh_token.user_id.id != user_id:
            raise AccessError(_("Invalid refresh token for this user."))
        if refresh_token.revoked:
            raise AccessDenied(_("Refresh token has been revoked."))
        return refresh_token