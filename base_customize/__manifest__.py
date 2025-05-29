# -*- coding: utf-8 -*-
# Part of RMXYZ. See LICENSE file for full copyright and licensing details.
{
    'name': 'Base (RMXYZ)',
    'version': '0.1',
    'author': 'Rangga Maulana',
    'summary': 'Customization base module',
    'description': """
This module is for customizing the odoo community
=================================================
Customization default odoo base
    """,
    'category': 'Customization/Base',
    'website': 'https://www.ranggamaulana.xyz',
    'depends': ['base_setup', 'base'],
    'data': [
        'views/ir_module_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'Other proprietary',
}
