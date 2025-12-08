# -*- coding: utf-8 -*-
# Part of RMXYZ. See LICENSE file for full copyright and licensing details.

{
    "name": "Web (XYZ)",
    "category": "XYZ/Base",
    "version": "1.0",
    "author": "Rangga Maulana",
    "description": """
Odoo Customize Web core module.
================================

This module provides the customize core of the Odoo Web Client.
""",
    "depends": ["xyz", "web"],
    "auto_install": True,
    "data": ["data/ir_config_parameter_data.xml", "views/ir_config_parameter_views.xml", "views/webclient_templates.xml"],
    "bootstrap": True,  # load translations for login screen,
    "assets": {
        "web._assets_primary_variables": [
            ("prepend", "web/static/src/scss/primary_variables.scss"),
            ("prepend", "xyz_web/static/src/scss/primary_variables.scss"),
        ],
        "web.assets_backend": [
            ("replace", "web/static/src/webclient/navbar/navbar.variables.scss", "xyz_web/static/src/webclient/navbar/navbar.variables.scss"),
            "xyz_web/static/src/views/form/reload_form_controller.js",
            "xyz_web/static/src/scss/xyz_web.scss",
            "xyz_web/static/src/webclient/navbar/navbar.scss",
            "xyz_web/static/src/webclient/navbar/navbar.xml",
            "xyz_web/static/src/views/form/form.variables.scss",
            "xyz_web/static/src/webclient/user_menu/user_menu.xml",
            "xyz_web/static/src/webclient/user_menu/user_menu_items.js",
            "xyz_web/static/src/webclient/switch_company_menu/switch_company_menu.xml",
            "xyz_web/static/src/webclient/search/search_systray.js",
            "xyz_web/static/src/webclient/search/search_systray.xml",
        ],
    },
    "license": "LGPL-3",
}
