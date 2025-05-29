# -*- coding: utf-8 -*-
# Part of RMXYZ. See LICENSE file for full copyright and licensing details.

{
    "name": "Web (RMXYZ)",
    "category": "Customization/Base",
    "version": "1.0",
    "author": "Rangga Maulana",
    "description": """
Odoo Customize Web core module.
========================

This module provides the customize core of the Odoo Web Client.
""",
    "depends": ["base_customize", "web"],
    "auto_install": True,
    "data": ["data/ir_config_parameter_data.xml", "views/ir_config_parameter_views.xml"],
    "bootstrap": True,  # load translations for login screen,
    "assets": {
        "web._assets_primary_variables": [
            ("prepend", "web/static/src/scss/primary_variables.scss"),
            ("prepend", "web_customize/static/src/scss/primary_variables.scss"),
        ],
        "web.assets_backend": [
            ("replace", "web/static/src/webclient/navbar/navbar.variables.scss", "web_customize/static/src/webclient/navbar/navbar.variables.scss"),
            "web_customize/static/src/webclient/navbar/navbar.scss",
            "web_customize/static/src/webclient/navbar/navbar.xml",
            "web_customize/static/src/views/form/form.variables.scss",
            "web_customize/static/src/webclient/user_menu/user_menu_items.js",
            "web_customize/static/src/views/form/reload_form_controller.js",
        ],
    },
    "license": "LGPL-3",
}
