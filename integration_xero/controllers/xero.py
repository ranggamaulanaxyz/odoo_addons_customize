from odoo import http


class XeroController(http.Controller):
    @http.route("/xero/callback")
    def callback(self):
        http.request.env['bus.bus']._sendone('on_xero_aunthentication', 'success', {'message': 'nice'})
        return http.request.render('integration_xero.callback')