# -*- coding: utf-8 -*-
# Part of RMXYZ. See LICENSE file for full copyright and licensing details.
{
    'name': 'Customer Portal (RMXYZ)',
    'summary': 'Customer Portal',
    'sequence': 9000,
    'category': 'Customization/Base',
    'description': """
This module adds required base code for a fully integrated customer portal.
It contains the base controller class and base templates. Business addons
will add their specific templates and controllers to extend the customer
portal.

This module contains most code coming from odoo v10 website_portal. Purpose
of this module is to allow the display of a customer portal without having
a dependency towards website editing and customization capabilities.""",
    'author': 'Rangga Maulana',
    'depends': ['web_customize', 'http_routing', 'mail', 'auth_signup', 'portal'],
    'data': [
        'views/portal_templates.xml',
    ],
    'assets': {},
    'auto_install': True,
    'license': 'Other proprietary',
}
