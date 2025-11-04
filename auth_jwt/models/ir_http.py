import re
from odoo import models
from odoo.http import request
from odoo.exceptions import AccessDenied
from werkzeug.datastructures import WWWAuthenticate
from werkzeug.exceptions import Unauthorized

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _auth_method_jwt(cls):
        headers = request.httprequest.headers
        def get_http_authorization_bearer_token():
            # werkzeug<2.3 doesn't expose `authorization.token` (for bearer authentication)
            # check header directly
            header = headers.get("Authorization")
            if header and (m := re.match(r"^bearer\s+(.+)$", header, re.IGNORECASE)):
                return m.group(1)
            return None
        
        if token := get_http_authorization_bearer_token():
            payload = request.env['res.users']._jwt_decode_token(token)
            uid = payload.get('sub')
            if not uid:
                raise Unauthorized("Invalid authentication token", www_authenticate=WWWAuthenticate('bearer'))
            if request.env.uid and request.env.uid != uid:
                raise AccessDenied("Session user does not match the used apikey.")
            request.update_env(user=uid)
            request.session.can_save = False
        elif not request.env.uid:
            e = "User not authenticated, use an API Key with a Bearer Authorization header."
            raise Unauthorized(e, www_authenticate=WWWAuthenticate('bearer'))
        
        cls._auth_method_user()