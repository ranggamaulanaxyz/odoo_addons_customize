{
    'name': 'JWT Authentication',
    'category': 'Hidden/Tools',
    'summary': 'Provides JSON Web Token (JWT) based authentication for secure API access in Odoo.',
    'website': 'https://www.ranggamaulana.xyz',
    'depends': ['base', 'base_setup'],
    'external_dependencies': {
        'python': ['pyjwt'],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'author': 'Rangga Maulana',
    'license': 'Other proprietary',
}