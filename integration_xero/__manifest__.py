# -*- coding: utf-8 -*-
# Part of RMXYZ. See LICENSE file for full copyright and licensing details.

{
    'name': 'XERO Integration',
    'category': 'Accounting/Accounting',
    'version': '1.0',
    'author': 'Rangga Maulana',
    'description': """
XERO Integration
========================

This module provides a seamless integration between Odoo Accounting and Xero.
It enables businesses to synchronize financial data securely and efficiently
across both systems, ensuring consistency and reducing manual reconciliation work.

Key Features
------------------------
- Connect Odoo with Xero using secure API authentication
- Synchronize Chart of Accounts, Taxes, and Journals
- Import Xero Invoices, Bills, Payments, and Contacts into Odoo
- Export Odoo Invoices, Bills, and Payments to Xero
- Automated periodic sync or manual synchronization options
- Detailed logs and error reporting for each sync activity
- Configuration options through Settings for simplified setup

Benefits
------------------------
- Eliminates double data entry between systems
- Improves accuracy of accounting records
- Reduces reconciliation time and operational overhead
- Ensures real-time alignment between Odoo and Xero financials

This module is ideal for organizations that use Odoo operationally while relying
on Xero for statutory accounting or external financial reporting.
""",
    'depends': ['xyz', 'xyz_account', 'bus'],
    'auto_install': False,
    'installable': True,
    'application': False,
    'data': [
        'views/templates.xml',
        'views/user_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'integration_xero/static/src/client_actions/xero/oauth.js',
        ]
    },
    'license': "Other proprietary",
}
