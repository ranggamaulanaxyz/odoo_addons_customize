# -*- coding: utf-8 -*-

from odoo.addons.web.controllers.webmanifest import WebManifest
from odoo.http import request

class WebManifest(WebManifest):
    def _get_webmanifest(self):
        web_app_name = request.env['ir.config_parameter'].sudo().get_param('web.web_app_name', 'Odoo')
        web_app_url = request.env['ir.config_parameter'].sudo().get_param('web.base.sorturl', 'odoo')
        web_app_background_color = request.env['ir.config_parameter'].sudo().get_param('web.web_app_background_color', '#714B67')
        web_app_theme_color = request.env['ir.config_parameter'].sudo().get_param('web.web_app_theme_color', '#714B67')
        manifest = {
            'name': web_app_name,
            'scope': '/' + web_app_url,
            'start_url': '/' + web_app_url,
            'display': 'standalone',
            'background_color': web_app_background_color,
            'theme_color': web_app_theme_color,
            'prefer_related_applications': False,
        }
        icon_sizes = ['192x192', '512x512']
        manifest['icons'] = [{
            'src': '/web/static/img/odoo-icon-%s.png' % size,
            'sizes': size,
            'type': 'image/png',
        } for size in icon_sizes]
        manifest['shortcuts'] = self._get_shortcuts()
        return manifest