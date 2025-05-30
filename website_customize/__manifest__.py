# -*- encoding: utf-8 -*-
# Part of RMXYZ. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website (RMXYZ)',
    'category': 'Customization/Website',
    'sequence': 20,
    'summary': 'Website customize',
    'version': '1.0',
    'depends': ['base_customize', 'website'],
    'auto_install': True,
    'installable': True,
    'data': [
        'views/webclient_templates.xml',
        'views/website_views.xml',
    ],
    'license': 'LGPL-3',
}
