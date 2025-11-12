from odoo import models, fields

class ApiApps(models.Model):
    _name = 'api.apps'

    name = fields.Char("Name", required=True, index=True, copy=False, tracking=True)
    company_id = fields.Many2one("res.company", "Company", required=True, tracking=True, default=lambda self: self.env.company)