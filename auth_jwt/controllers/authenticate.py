from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied, UserError
from .controller import Controller
import logging

_logger = logging.getLogger(__name__)

class AuthenticateController(Controller):
    @http.route('/api/authenticate', type="json2", auth="none", methods=['POST'], csrf=False)
    def authenticate(self, **kwargs):
        credential = {'login': kwargs.get('login'), 'password': kwargs.get('password'), 'type': 'password', 'mfa': 'skip'}
        auth_info = request.session.authenticate(request.env, credential)
        user = request.env['res.users'].browse(auth_info['uid'])
        access_token = user._jwt_generate_access_token()
        refresh_token = user._jwt_generate_refresh_token()
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    @http.route('/api/token/update', type="json2", auth="none", methods=['POST'], csrf=False)
    def update(self, **kwargs):
        refresh_token = kwargs.get('refresh_token')

        # 1. Input Validation
        if not refresh_token:
            return self._response_error(400, "Missing refresh_token")

        try:
            # 2. Decode Token (Wrap in try/except)
            # Assuming _jwt_decode_token raises exceptions on failure
            payload = request.env['res.users'].sudo()._jwt_decode_token(refresh_token)
            
            uid = int(payload.get("sub"))
            token_id = payload.get("jti")

            # 3. Verify User Exists and is Active
            user = request.env['res.users'].sudo().browse(uid)
            if not user.exists() or not user.active:
                _logger.warning(f"Token refresh attempted for inactive user: {uid}")
                return self._response_error(401, "User inactive or deleted")

            # 4. Generate New Tokens
            # Reusing token_id (jti) implies you are rotating the token 
            # while maintaining the same session/family.
            new_access_token = user._jwt_generate_access_token()
            new_refresh_token = user._jwt_generate_refresh_token(token_id)

            return self._response_success(200, data={
                "access_token": new_access_token,
                "refresh_token": new_refresh_token
            })

        except AccessDenied:
            return self._response_error(401, "Invalid or expired token")
        except Exception as e:
            _logger.error(f"Token refresh error: {str(e)}")
            return self._response_error(500, "Internal Server Error")
    
    @http.route('/api/token/revoke', type="json2", auth="jwt", methods=['POST'], csrf=False)
    def revoke(self, **kwargs):
        refresh_token = kwargs.get('refresh_token')
        if not refresh_token:
            return {"message": "Refresh token is not provided"}
        payload = request.env['res.users']._jwt_decode_token(refresh_token)
        token_id = payload.get("jti")
        Token = request.env['res.users.jwt.refresh']
        token = Token._browse_token(request.env.uid, token_id)
        if not token:
            return {"message": "Refresh token is not found"}
        token.write({'revoked': True})
        return {"message": "Success"}