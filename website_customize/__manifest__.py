# -*- encoding: utf-8 -*-
# Part of RMXYZ. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website (RMXYZ)',
    'category': 'Customization/Website',
    'sequence': 20,
    'summary': 'Website customize',
    'version': '1.0',
    'author': 'Rangga Maulana',
    'depends': ['base_customize', 'website'],
    'auto_install': True,
    'installable': True,
    'data': [
        'views/webclient_templates.xml',
        'views/website_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'website_customize/static/src/client_actions/website_preview/website_builder_actions.js',
        ]
    },
    'license': 'LGPL-3',
}
