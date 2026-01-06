# -*- coding: utf-8 -*-
# Part of RMXYZ. See LICENSE file for full copyright and licensing details.

{
    'name': 'Accounting (XYZ)',
    'category': 'Accounting/Accounting',
    'version': '1.0',
    'author': 'Rangga Maulana',
    'description': """
Accounting Module
========================x

This module provides the accounting feature.
""",
    'depends': ['account'],
    'auto_install': False,
    'installable': True,
    'application': False,
    'data': [
        'security/account_security.xml',
        'views/bank_statement_views.xml',
        'views/bank_statement_line_views.xml',
        'views/res_config_settings_views.xml',
        'views/menu_item_views.xml',
    ],
    'license': 'LGPL-3',
}
