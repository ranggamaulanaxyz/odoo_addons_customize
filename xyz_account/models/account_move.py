from odoo import models, fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    move_attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'account.move.line')], string='Move Attachment')