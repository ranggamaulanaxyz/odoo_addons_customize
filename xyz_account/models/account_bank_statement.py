from odoo import models

class BankStatement(models.Model):
    _name = 'account.bank.statement'
    _inherit = ['account.bank.statement', 'mail.thread', 'mail.activity.mixin']
    
    def action_open_statement_lines(self):
        self.ensure_one()
        if not self:
            return {}
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "account_statement_base.account_bank_statement_line_action"
        )
        action.update(
            {
                "domain": [("statement_id", "=", self.id)],
                "context": {
                    "default_statement_id": self.id,
                    "default_journal_id": self._context.get("active_id")
                    if self._context.get("active_model") == "account.journal"
                    else None,
                    "account_bank_statement_line_main_view": True,
                },
            }
        )

        return action

    def open_entries(self):
        self.ensure_one()
        return {
            "name": self.env._("Journal Items"),
            "view_mode": "list,form",
            "res_model": "account.move.line",
            "view_id": False,
            "type": "ir.actions.act_window",
            "context": {"search_default_group_by_move": 1, "expand": 1},
            "search_view_id": self.env.ref("account.view_account_move_line_filter").id,
            "domain": [
                "&",
                ("parent_state", "=", "posted"),
                ("statement_id", "=", self.id),
            ],
        }

    def action_open_bank_reconcile_widget(self):
        """
        Open the bank reconciliation widget for this statement's journal.
        """
        self.ensure_one()
        return self.journal_id.action_open_bank_reconciliation()

    def action_open_journal_invalid_statements(self):
        """
        Open a list view showing invalid statements for this statement's journal.
        """
        self.ensure_one()
        return {
            'name': self.env._('Invalid Statements'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.bank.statement',
            'view_mode': 'list,form',
            'domain': [
                ('journal_id', '=', self.journal_id.id),
                '|',
                ('is_valid', '=', False),
                ('is_complete', '=', False),
            ],
            'context': {'search_default_journal_id': self.journal_id.id},
        }