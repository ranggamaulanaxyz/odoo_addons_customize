from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons.base.models.ir_model import FIELD_TYPES

class IntegrationApplication(models.Model):
    _name = 'integration.application'
    _description = 'Application'

    name = fields.Char("Name", required=True, index=True, copy=False, tracking=True)
    company_id = fields.Many2one("res.company", "Company", required=True, tracking=True, default=lambda self: self.env.company)
    parameter_count = fields.Integer("Parameter Count", compute='_compute_parameter_count')
    parameter_ids = fields.One2many('integration.application.parameter', 'integration_application_id', string="Parameters")
    
    def get_parameter(self, key):
        self.ensure_one()
        value = self.env['integration.application.parameter'].get_parameter_value(key, self.id)
        return value or False

    def open_parameters(self):
        self.ensure_one()
        return {
            'name': _('Parameters'),
            'type': 'ir.actions.act_window',
            'res_model': 'integration.application.parameter',
            'view_mode': 'list,form',
            'domain': [('integration_application_id', '=', self.id)],
            'context': {'default_integration_application_id': self.id},
        }

    @api.depends('parameter_ids')
    def _compute_parameter_count(self):
        domain = [('integration_application_id', 'in', self.ids)]
        counts_data = self.env['integration.application.parameter']._read_group(domain, ['integration_application_id'], ['__count'])
        mapped_counts_data = dict(counts_data)
        for record in self:
            record.parameter_count = mapped_counts_data.get(record, 0)

class IntegrationApplicationParameter(models.Model):
    _name = 'integration.application.parameter'
    _description = 'Application Parameter'

    integration_application_id = fields.Many2one("integration.application", "Application", required=True)
    type = fields.Selection(FIELD_TYPES, string='Field Type', required=True, default='char')
    key = fields.Char('Key', required=True, index=True)
    value = fields.Char('Value', compute='_compute_value')
    value_char = fields.Char('Value (Char)', exportable=False)
    value_text = fields.Text('Value (Text)', exportable=False)
    value_integer = fields.Integer('Value (Integer)', exportable=False)
    value_float = fields.Float('Value (Float)', exportable=False)

    @api.depends('type', 'value_char', 'value_text')
    def _compute_value(self):
        for record in self:
            record.value = record.get_value()

    @api.constrains('key', 'integration_application_id')
    def _constrains_unique(self):
        for record in self:
            domain = [
                ('key', '=', record.key),
                ('integration_application_id', '=', record.integration_application_id),
                ('id', '!=', record.id),
            ]
            if self.search_count(domain) > 0:
                raise UserError(_("This parameter key already exists."))
            
    def get_value(self):
        if self.type == 'text':
            return self.value_text
        if self.type == 'integer':
            return self.value_integer
        if self.type == 'float':
            return self.value_float
        return self.value_char

    def get_parameter_value(self, key, integration_application_id):
        return self.search([('key', '=', key), ('integration_application_id', '=', integration_application_id)], limit=1)