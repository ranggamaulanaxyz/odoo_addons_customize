from odoo import http
import time


class XeroController(http.Controller):
    @http.route("/xero/callback", type='http', auth='user')
    def callback(self):
        time.sleep(5)
        http.request.env.user.write({'name': 'Rangga Maulana'})
        http.request.env['bus.bus']._sendone('on_xero_authentication', 'status', {'message': 'nice'})
        
        
        return http.request.render('integration_xero.callback')