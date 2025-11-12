from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import Home
from odoo.addons.web.controllers.utils import is_user_internal

class CustomizeHome(Home):
    @http.route('/', type='http', auth="none")
    def index(self, s_action=None, db=None, **kw):
        if request.db and request.session.uid and not is_user_internal(request.session.uid):
            return request.redirect_query('/web/login_successful', query=request.params)
        config_parameter = request.env['ir.config_parameter']
        sorturl = config_parameter.sudo().get_param("web.base.sorturl", "odoo")
        return request.redirect_query('/' + sorturl, query=request.params)