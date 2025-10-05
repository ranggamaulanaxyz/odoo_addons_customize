# -*- coding: utf-8 -*-
# Part of RMXYZ. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Digital (RMXYZ)',
    'category': 'Sales/Sales',
    'version': '1.0',
    'author': 'Rangga Maulana',
    'description': """
Product Digital Module
========================

This module provides the digital product feature.
""",
    'depends': ['base', 'product'],
    'auto_install': False,
    'installable': True,
    'application': False,
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/product_digital_provider_views.xml',
        'views/product_digital_token_views.xml',
        'views/product_digital_transaction_views.xml',
    ],
    'author': 'Rangga Maulana',
    'license': 'Other proprietary',
}
