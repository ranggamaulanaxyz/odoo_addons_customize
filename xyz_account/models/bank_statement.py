from odoo import models

class BankStatement(models.Model):
 _name = 'account.bank.statement'
 _inherit = ['account.bank.statement', 'mail.thread', 'mail.activity.mixin']