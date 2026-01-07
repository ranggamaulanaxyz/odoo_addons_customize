from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    def get_total_journal_amount(self):
        """
        Compute and return the total amounts for each journal.
        Returns a dictionary with:
        - balance_amount: Formatted current balance for bank/cash/credit journals
        - has_invalid_statements: Boolean indicating if there are invalid statements
        - available_balance_amount: Formatted available balance (outstanding payments)
        """
        self.ensure_one()
        self.env['account.move'].flush_model()
        self.env['account.move.line'].flush_model()

        currency = self.currency_id or self.company_id.sudo().currency_id
        
        result = {
            'balance_amount': '',
            'has_invalid_statements': False,
            'available_balance_amount': '',
        }

        if self.type in ('bank', 'cash', 'credit'):
            # Get current statement balance
            balance = self._get_journal_balance()
            result['balance_amount'] = currency.format(balance) if balance else ''
            
            # Check for invalid statements
            result['has_invalid_statements'] = self.has_invalid_statements
            
            # Get outstanding payments balance (available balance)
            outstanding_balance = self._get_outstanding_payments_balance()
            result['available_balance_amount'] = currency.format(outstanding_balance) if outstanding_balance else ''

        return result

    def _get_journal_balance(self):
        """Get the current balance for a bank/cash/credit journal."""
        self.ensure_one()
        self.env.cr.execute("""
            SELECT COALESCE(statement.balance_end_real, 0) AS balance_end_real,
                   COALESCE(without_statement.amount, 0) AS unlinked_amount
              FROM account_journal journal
         LEFT JOIN LATERAL (
                       SELECT id,
                              first_line_index,
                              balance_end_real
                         FROM account_bank_statement
                        WHERE journal_id = journal.id
                          AND company_id = ANY(%s)
                          AND first_line_index IS NOT NULL
                     ORDER BY date DESC, id DESC
                        LIMIT 1
               ) statement ON TRUE
         LEFT JOIN LATERAL (
                       SELECT COALESCE(SUM(stl.amount), 0.0) AS amount
                         FROM account_bank_statement_line stl
                         JOIN account_move move ON move.id = stl.move_id
                        WHERE stl.statement_id IS NULL
                          AND move.state != 'cancel'
                          AND stl.journal_id = journal.id
                          AND stl.company_id = ANY(%s)
                          AND stl.internal_index >= COALESCE(statement.first_line_index, '')
                        LIMIT 1
               ) without_statement ON TRUE
             WHERE journal.id = %s
        """, [self.env.companies.ids, self.env.companies.ids, self.id])

        row = self.env.cr.dictfetchone()
        if row:
            return row['balance_end_real'] + row['unlinked_amount']
        return 0.0

    def _get_outstanding_payments_balance(self):
        """Get outstanding payments balance for a bank/cash/credit journal."""
        self.ensure_one()
        self.env.cr.execute("""
            SELECT SUM(CASE
                       WHEN payment.payment_type = 'outbound' THEN -payment.amount
                       ELSE payment.amount
                   END) AS outstanding_balance
              FROM account_payment payment
              JOIN account_move move ON move.origin_payment_id = payment.id
             WHERE payment.is_matched IS NOT TRUE
               AND move.state = 'posted'
               AND payment.journal_id = %s
               AND payment.company_id = ANY(%s)
        """, [self.id, self.env.companies.ids])

        row = self.env.cr.dictfetchone()
        return row['outstanding_balance'] if row and row['outstanding_balance'] else 0.0

    def _compute_bank_cash_total(self, result, journals):
        """Compute total balance for bank/cash/credit type journals."""
        # Get the current statement balance for bank/cash journals
        self.env.cr.execute("""
            SELECT journal.id AS journal_id,
                   COALESCE(statement.balance_end_real, 0) AS balance_end_real,
                   COALESCE(without_statement.amount, 0) AS unlinked_amount
              FROM account_journal journal
         LEFT JOIN LATERAL (
                       SELECT id,
                              first_line_index,
                              balance_end_real
                         FROM account_bank_statement
                        WHERE journal_id = journal.id
                          AND company_id = ANY(%s)
                          AND first_line_index IS NOT NULL
                     ORDER BY date DESC, id DESC
                        LIMIT 1
               ) statement ON TRUE
         LEFT JOIN LATERAL (
                       SELECT COALESCE(SUM(stl.amount), 0.0) AS amount
                         FROM account_bank_statement_line stl
                         JOIN account_move move ON move.id = stl.move_id
                        WHERE stl.statement_id IS NULL
                          AND move.state != 'cancel'
                          AND stl.journal_id = journal.id
                          AND stl.company_id = ANY(%s)
                          AND stl.internal_index >= COALESCE(statement.first_line_index, '')
                        LIMIT 1
               ) without_statement ON TRUE
             WHERE journal.id = ANY(%s)
        """, [self.env.companies.ids, self.env.companies.ids, journals.ids])

        for row in self.env.cr.dictfetchall():
            journal_id = row['journal_id']
            result[journal_id]['total_balance'] = row['balance_end_real'] + row['unlinked_amount']

    def _compute_sale_purchase_total(self, result, journals):
        """Compute total draft and to_pay amounts for sale/purchase journals."""
        # Draft amounts
        self.env.cr.execute("""
            SELECT journal_id,
                   SUM(CASE WHEN move_type IN ('out_refund', 'in_refund') THEN -1 ELSE 1 END * amount_total_signed) AS total_draft
              FROM account_move
             WHERE journal_id = ANY(%s)
               AND company_id = ANY(%s)
               AND state = 'draft'
               AND move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
          GROUP BY journal_id
        """, [journals.ids, self.env.companies.ids])

        for row in self.env.cr.dictfetchall():
            journal = self.browse(row['journal_id'])
            sign = 1 if journal.type == 'sale' else -1
            result[row['journal_id']]['total_draft'] = sign * (row['total_draft'] or 0.0)

        # To pay amounts (posted, not fully paid)
        self.env.cr.execute("""
            SELECT journal_id,
                   SUM(amount_residual_signed) AS total_to_pay
              FROM account_move
             WHERE journal_id = ANY(%s)
               AND company_id = ANY(%s)
               AND state = 'posted'
               AND payment_state IN ('not_paid', 'partial')
               AND move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund')
          GROUP BY journal_id
        """, [journals.ids, self.env.companies.ids])

        for row in self.env.cr.dictfetchall():
            journal = self.browse(row['journal_id'])
            sign = 1 if journal.type == 'sale' else -1
            result[row['journal_id']]['total_to_pay'] = sign * (row['total_to_pay'] or 0.0)

    def action_open_bank_reconciliation(self):
        """
        Open the bank reconciliation widget for this journal.
        """
        self.ensure_one()
        return {
            'name': self.name,
            'type': 'ir.actions.client',
            'tag': 'bank_rec_widget',
            'context': {
                'active_id': self.id,
                'active_model': 'account.journal',
                'default_journal_id': self.id,
            },
        }