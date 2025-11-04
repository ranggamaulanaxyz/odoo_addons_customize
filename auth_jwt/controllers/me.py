from odoo import http
from odoo.http import request

class MeController(http.Controller):
    @http.route('/api/me', type="json2", auth="jwt", methods=['GET'], csrf=False)
    def me(self, **kwargs):
        user = request.env.user
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }