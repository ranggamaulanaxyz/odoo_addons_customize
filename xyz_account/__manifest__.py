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
    "assets": {
        "web.assets_backend": [
            "xyz_account/static/src/components/bank_reconciliation/bank_reconciliation_widget.scss",
            "xyz_account/static/src/components/bank_reconciliation/bank_reconciliation_service.js",
            "xyz_account/static/src/components/bank_reconciliation/button/button.js",
            "xyz_account/static/src/components/bank_reconciliation/button/button.xml",
            "xyz_account/static/src/components/bank_reconciliation/file_uploader/file_uploader.js",
            "xyz_account/static/src/components/bank_reconciliation/search_dialog/search_dialog.js",
            "xyz_account/static/src/components/bank_reconciliation/search_dialog/search_dialog.xml",
            "xyz_account/static/src/components/bank_reconciliation/bankrec_form_dialog/bankrec_form_dialog.js",
            "xyz_account/static/src/components/bank_reconciliation/bankrec_form_dialog/bankrec_form_dialog.xml",
            "xyz_account/static/src/components/bank_reconciliation/line_info_pop_over/line_info_pop_over.js",
            "xyz_account/static/src/components/bank_reconciliation/line_info_pop_over/line_info_pop_over.xml",
            "xyz_account/static/src/components/bank_reconciliation/button_list/button_list.xml",
            "xyz_account/static/src/components/bank_reconciliation/button_list/button_list.js",
            "xyz_account/static/src/components/bank_reconciliation/button_list/button_list.xml",
            "xyz_account/static/src/components/bank_reconciliation/line_to_reconcile/line_to_reconcile.js",
            "xyz_account/static/src/components/bank_reconciliation/line_to_reconcile/line_to_reconcile.xml",
            "xyz_account/static/src/components/bank_reconciliation/reconciled_line_name/reconciled_line_name.js",
            "xyz_account/static/src/components/bank_reconciliation/reconciled_line_name/reconciled_line_name.xml",
            "xyz_account/static/src/components/bank_reconciliation/statement_summary/statement_summary.js",
            "xyz_account/static/src/components/bank_reconciliation/statement_summary/statement_summary.xml",
            "xyz_account/static/src/components/bank_reconciliation/statement_line/statement_line.js",
            "xyz_account/static/src/components/bank_reconciliation/statement_line/statement_line.xml",
            "xyz_account/static/src/components/bank_reconciliation/chatter/chatter.js",
            "xyz_account/static/src/components/bank_reconciliation/quick_create/quick_create.js",
            "xyz_account/static/src/components/bank_reconciliation/quick_create/quick_create.xml",
            "xyz_account/static/src/components/bank_reconciliation/kanban_controller.xml",
            "xyz_account/static/src/components/bank_reconciliation/kanban_controller.js",
            "xyz_account/static/src/components/bank_reconciliation/kanban_renderer.xml",
            "xyz_account/static/src/components/bank_reconciliation/kanban_renderer.js",
        ],
    },
    'license': 'LGPL-3',
}
