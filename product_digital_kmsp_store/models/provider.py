from odoo import models, fields
import requests

class ProductDigitalProvider(models.Model):
    _inherit = 'product.digital.provider'

    type = fields.Selection(selection_add=[('kmsp_store', 'KMSP Store')], ondelete={'kmsp_store': 'set default'})
    api_key = fields.Char(string='API Key')

    def _kmsp_store_sync_products(self):
        ProductTemplate = self.env['product.template']
        for record in self:
            endpoint = "https://golang-openapi-packagelist-xltembakservice.kmsp-store.com/v1?api_key=586e4aeb-0202-48fc-96f4-06f57c650345"
            # endpoint = f"https://golang-openapi-packagelist-xltembakservice.kmsp-store.com/v1?api_key={record.api_key}"
            response = requests.get(endpoint)
            if response.status_code != 200:
                response.raise_for_status()
            result = response.json()
            data = result.get('data', [])
            for product_data in data:
                values = {
                    'name': product_data.get('package_name'),
                    'default_code': product_data.get('package_code'),
                    'description': product_data.get('package_description'),
                    'list_price': product_data.get('package_harga_int'),
                    'standard_price': product_data.get('package_harga_int'),
                    'is_digital': True,
                    'product_digital_provider_id': record.id,
                }
                product = ProductTemplate.search([('default_code', '=', product_data.get('package_code')), ('product_digital_provider_id', '=', record.id)], limit=1)
                if product:
                    if product.list_price < product_data.get('package_harga_int'):
                        product.write({'list_price': product_data.get('package_harga_int')})
                    product.write(values)
                else:
                    ProductTemplate.create(values)