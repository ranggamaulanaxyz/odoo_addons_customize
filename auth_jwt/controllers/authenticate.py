from odoo import http
from odoo.http import request

class AuthenticateController(http.Controller):
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
        payload = request.env['res.users']._jwt_decode_token(refresh_token)
        uid = int(payload.get("sub"))
        token_id = payload.get("jti")
        user = request.env['res.users'].sudo().browse(uid)
        access_token = user._jwt_generate_access_token()
        refresh_token = user._jwt_generate_refresh_token(token_id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
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