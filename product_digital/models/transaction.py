from odoo import models, fields

class ProductDigitalTransaction(models.Model):
    _name = "product.digital.transaction"
    _description = "Product Digital Transaction"

    provider_id = fields.Many2one("product.digital.provider", "Product Digital Provider", required=True, ondelete="restrict")
    product_id = fields.Many2one("product.product", "Product", required=True, ondelete="restrict")
    partner_id = fields.Many2one("res.partner", "Customer", required=True, ondelete="restrict")
    access_token_id = fields.Many2one("product.digital.token", string="Access Token", ondelete="restrict")
    state = fields.Selection([("draft", "Draft"), ("pending", "Pending"), ("error", "Error"), ("done", "Success"), ("cancel", "Canceled")], string="Status", default="draft", required=True)