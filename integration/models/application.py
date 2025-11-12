from odoo import models, fields, api, _
from odoo.exceptions import UserError

class IntegrationApplication(models.Model):
    _name = 'integration.application'
    _description = 'Application'

    name = fields.Char("Name", required=True, index=True, copy=False, tracking=True)
    company_id = fields.Many2one("res.company", "Company", required=True, tracking=True, default=lambda self: self.env.company)
    
    def get_parameter(self, key):
        self.ensure_one()
        value = self.env['integration.application.parameter'].get_parameter_value(key, self.id)
        return value or False

class IntegrationApplicationParameter(models.Model):
    _name = 'integration.application.parameter'
    _description = 'Application Parameter'

    integration_application_id = fields.Many2one("integration.application", "Application", required=True)
    key = fields.Char("Key", requried=True, index=True)
    value = fields.Char("Value")

    @api.constrains('key', 'integration_application_id')
    def _constrains_unique(self):
        params = self.search([('key', '=', self.key), ('integration_application_id', '=', self.integration_application_id)], limit=1)
        if params.exists():
            raise UserError(_("This parameter key already exists."))

    def get_parameter_value(self, key, integration_application_id):
        return self.search([('key', '=', key), ('integration_application_id', '=', integration_application_id)], limit=1)