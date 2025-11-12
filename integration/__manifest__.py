{
    'name': "Api Management",
    'version': "1.0",
    'description': """
API Management
==============
This module provides a centralized interface to manage all API settings and related features. 
Key capabilities include endpoint configuration, API key and JWT token management, authentication and access control, as well as rate limiting and CORS policies. It also includes logging and auditing mechanisms to record API requests, credential history, and basic usage statistics. The module defines data models to persist configuration, wizards and admin forms for quick setup, and backend menus for managing users, roles, and permissions integrated with auth_jwt. Designed to simplify creation, updating, rotation, and deactivation of credentials while improving security and observability for both internal and third-party APIs.
""",
    'author': "Rangga Maulana",
    'website': "https://www.ranggamaulana.xyz",
    'license': "Other proprietary",
    'category': "Administration/Administration",
    'depends': ['base', 'web', 'auth_jwt'],
    'data': [
        'security/integration_security.xml',
        'security/integration_rules.xml',
        'security/ir.model.access.csv',

        'views/application_views.xml',
    ],
    'demo': [],
    'auto_install': False,
    'application': True,
}