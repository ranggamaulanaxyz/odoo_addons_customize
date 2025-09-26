from odoo import models, fields

class ProductDigitalProvider(models.Model):
    _name = 'product.digital.provider'
    _description = 'Product Digital Provider'

    name = fields.Char(string='Provider Name', required=True, index=True)
    type = fields.Selection([('internal', 'Internal')], string='Provider Type', required=True, default='internal')
    active = fields.Boolean(string='Active', default=True)

    def sync_products(self):
        name = "_%s_sync_products" % self.type
        if hasattr(self, name):
            return getattr(self, name)()
        else:
            raise models.ValidationError("Sync method not implemented for provider type '%s'" % self.type)