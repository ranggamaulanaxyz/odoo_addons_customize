from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_digital = fields.Boolean(string='Is a Digital Product', default=False, help='Indicates if the product is a digital product.')
    product_digital_provider_id = fields.Many2one('product.digital.provider', string='Digital Product Provider')