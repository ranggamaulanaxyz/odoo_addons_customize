# -*- coding: utf-8 -*-

import mimetypes
from odoo.addons.web.controllers.webmanifest import WebManifest
from odoo.exceptions import AccessError
from odoo.http import request

class WebManifest(WebManifest):
    def _get_shortcuts(self):
        module_names = ['mail', 'crm', 'project', 'project_todo']
        try:
            module_ids = request.env['ir.module.module'].search([('state', '=', 'installed'), ('name', 'in', module_names)]) \
                                                        .sorted(key=lambda r: module_names.index(r["name"]))
        except AccessError:
            return []
        menu_roots = request.env['ir.ui.menu'].get_user_roots()
        datas = request.env['ir.model.data'].sudo().search([('model', '=', 'ir.ui.menu'),
                                                         ('res_id', 'in', menu_roots.ids),
                                                         ('module', 'in', module_names)])
        shortcuts = []
        for module in module_ids:
            data = datas.filtered(lambda res: res.module == module.name)
            if data:
                shortcuts.append({
                    'name': module.display_name,
                    'url': '/odoo?menu_id=%s' % data.mapped('res_id')[0],
                    'description': module.summary,
                    'icons': [{
                        'sizes': '100x100',
                        'src': module.icon,
                        'type': mimetypes.guess_type(module.icon)[0] or 'image/png'
                    }]
                })
        return shortcuts
    
    def _get_webmanifest(self):
        web_app_name = request.env['ir.config_parameter'].sudo().get_param('web.web_app_name', 'Odoo')
        web_app_url = request.env['ir.config_parameter'].sudo().get_param('web.base.sorturl', 'odoo')
        web_app_background_color = request.env['ir.config_parameter'].sudo().get_param('web.web_app_background_color', '#714B67')
        web_app_theme_color = request.env['ir.config_parameter'].sudo().get_param('web.web_app_theme_color', '#714B67')
        web_app_icon_path = request.env['ir.config_parameter'].sudo().get_param('web.web_app_icon_path', '/web/static/img/odoo-')
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
            'src': web_app_icon_path + 'icon-%s.png' % size,
            'sizes': size,
            'type': 'image/png',
        } for size in icon_sizes]
        manifest['shortcuts'] = self._get_shortcuts()
        return manifest