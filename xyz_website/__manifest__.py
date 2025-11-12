# -*- encoding: utf-8 -*-
# Part of RMXYZ. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website (XYZ)',
    'category': 'XYZ/Website',
    'sequence': 20,
    'summary': 'Website customize',
    'version': '1.0',
    'author': 'Rangga Maulana',
    'depends': ['xyz', 'website'],
    'auto_install': True,
    'installable': True,
    'data': [
        'views/webclient_templates.xml',
        'views/website_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'xyz_website/static/src/client_actions/website_preview/website_builder_actions.js',
        ]
    },
    'license': 'LGPL-3',
}
