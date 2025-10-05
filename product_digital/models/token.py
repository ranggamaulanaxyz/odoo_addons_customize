from odoo import models, fields

class ProductDigitalToken(models.Model):
    _name = "product.digital.token"
    _description = "Product Digital Access Token"
    _rec_name = "identifier"

    partner_id = fields.Many2one("res.partner", "Customer", required=True, ondelete="restrict")
    provider_id = fields.Many2one("product.digital.provider", required=True, ondelete="restrict")
    identifier = fields.Char("Identifier", required=True, help="MSISDN/Customer ID/etc")
    token = fields.Char("Access Token")