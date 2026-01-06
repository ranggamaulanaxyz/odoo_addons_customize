{
    'name': "Integration Blog Plugins",
    'version': "1.0",
    'description': """
Integration Blog Plugins
========================
Blog plugins for Integration addons
""",
    'author': "Rangga Maulana",
    'website': "https://www.ranggamaulana.xyz",
    'license': "Other proprietary",
    'category': "Integration/Blog",
    'depends': ['integration', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/article_views.xml',
    ],
    'demo': [],
    'auto_install': False,
    'application': True,
}