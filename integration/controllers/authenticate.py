from odoo import http
from odoo.addons.auth_jwt.controller import AuthenticateController

class IntegrationAuthenticateController(AuthenticateController):
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