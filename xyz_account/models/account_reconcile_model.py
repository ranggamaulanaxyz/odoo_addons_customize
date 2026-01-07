import re
from odoo import models

class AccountReconcileModel(models.Model):
    _inherit = 'account.reconcile.model'

    def get_available_reconcile_model_per_statement_line(self, st_lines=None):
        """
        Get available reconcile models for each statement line based on matching criteria.
        
        :param st_lines: recordset of account.bank.statement.line (optional)
                         If not provided, fetches all unreconciled statement lines for current company
        :return: dict mapping statement line ID (as string) to list of applicable reconcile models
                 {"st_line_id": [{"id": model_id, "display_name": model_name}, ...]}
        """
        if st_lines is None:
            # Fetch all unreconciled statement lines for the current company
            st_lines = self.env['account.bank.statement.line'].search([
                ('is_reconciled', '=', False),
                ('company_id', '=', self.env.company.id),
            ])
        
        if not st_lines:
            return {}
        
        result = {str(st_line.id): [] for st_line in st_lines}
        
        # Get all active reconcile models for the companies in the statement lines
        company_ids = st_lines.mapped('company_id').ids
        all_models = self.env['account.reconcile.model'].search([
            ('active', '=', True),
            ('company_id', 'in', company_ids),
        ])
        
        if not all_models:
            return result
        
        for st_line in st_lines:
            applicable_models = []
            
            for model in all_models.filtered(lambda m: m.company_id == st_line.company_id):
                if self._is_model_applicable_to_st_line(model, st_line):
                    applicable_models.append({
                        'id': model.id,
                        'display_name': model.display_name,
                    })
            
            result[str(st_line.id)] = applicable_models
        
        return result
    
    def _is_model_applicable_to_st_line(self, model, st_line):
        """
        Check if a reconcile model is applicable to a specific statement line.
        
        :param model: account.reconcile.model record
        :param st_line: account.bank.statement.line record
        :return: boolean
        """
        # Check journal match
        if model.match_journal_ids and st_line.journal_id not in model.match_journal_ids:
            return False
        
        # Check partner match
        if model.match_partner_ids and st_line.partner_id and st_line.partner_id not in model.match_partner_ids:
            return False
        
        # Check amount match
        amount = abs(st_line.amount)
        if model.match_amount:
            if model.match_amount == 'lower' and amount > model.match_amount_max:
                return False
            elif model.match_amount == 'greater' and amount < model.match_amount_min:
                return False
            elif model.match_amount == 'between':
                if amount < model.match_amount_min or amount > model.match_amount_max:
                    return False
        
        # Check label match
        if model.match_label and model.match_label_param:
            label_to_match = ' '.join([
                st_line.payment_ref or '',
                st_line.narration or '',
            ]).lower()
            param = model.match_label_param.lower() if model.match_label != 'match_regex' else model.match_label_param
            
            if model.match_label == 'contains':
                if param not in label_to_match:
                    return False
            elif model.match_label == 'not_contains':
                if param in label_to_match:
                    return False
            elif model.match_label == 'match_regex':
                try:
                    if not re.search(model.match_label_param, label_to_match, re.IGNORECASE):
                        return False
                except re.error:
                    return False
        
        return True

    def trigger_reconciliation_model(self, st_line_id, model_id=None):
        """
        Apply a reconciliation model to a statement line.
        
        :param st_line_id: ID of the bank statement line to reconcile
        :param model_id: ID of the reconcile model to apply (optional, uses self if not provided)
        :return: Empty dict for JSON-RPC response compatibility
        """
        st_line = self.env['account.bank.statement.line'].browse(st_line_id)
        if not st_line.exists():
            return {}
        
        model = self.browse(model_id) if model_id else self
        if not model.exists():
            return {}
        
        model = model[0] if len(model) > 1 else model
        
        # Get the suspense lines from the statement line's move
        _liquidity_lines, suspense_lines, _other_lines = st_line._seek_for_lines()
        
        if not suspense_lines:
            return {}
        
        suspense_line = suspense_lines[0]
        
        # Prepare new lines based on the reconcile model's line definitions
        from odoo import Command
        
        # Get the exact amounts from the suspense line to ensure balance
        total_amount_currency = suspense_line.amount_currency
        total_debit = suspense_line.debit
        total_credit = suspense_line.credit
        
        new_lines_vals = []
        used_amount_currency = 0.0
        used_debit = 0.0
        used_credit = 0.0
        
        model_lines = list(model.line_ids)
        
        for idx, line in enumerate(model_lines):
            is_last_line = (idx == len(model_lines) - 1)
            
            if is_last_line:
                # Last line takes the remaining balance to ensure entry is balanced
                line_amount_currency = total_amount_currency - used_amount_currency
                line_debit = total_debit - used_debit
                line_credit = total_credit - used_credit
            else:
                if line.amount_type == 'percentage':
                    ratio = line.amount / 100.0
                    line_amount_currency = total_amount_currency * ratio
                    line_debit = total_debit * ratio
                    line_credit = total_credit * ratio
                elif line.amount_type == 'fixed':
                    # Fixed amount - need to determine sign from statement line
                    if total_credit > 0:
                        line_debit = abs(line.amount)
                        line_credit = 0.0
                        line_amount_currency = abs(line.amount)
                    else:
                        line_debit = 0.0
                        line_credit = abs(line.amount)
                        line_amount_currency = -abs(line.amount)
                else:  # regex or remainder type
                    line_amount_currency = total_amount_currency - used_amount_currency
                    line_debit = total_debit - used_debit
                    line_credit = total_credit - used_credit
                
                used_amount_currency += line_amount_currency
                used_debit += line_debit
                used_credit += line_credit
            
            new_line_vals = {
                'name': line.label or model.name,
                'account_id': line.account_id.id,
                'partner_id': st_line.partner_id.id or False,
                'currency_id': suspense_line.currency_id.id,
                'amount_currency': line_amount_currency,
                'debit': line_debit,
                'credit': line_credit,
                'reconcile_model_id': model.id,
            }
            
            if line.analytic_distribution:
                new_line_vals['analytic_distribution'] = line.analytic_distribution
            
            new_lines_vals.append(new_line_vals)
        
        if not new_lines_vals:
            # If no model lines, create one line with the full suspense amount
            new_lines_vals.append({
                'name': model.name,
                'account_id': model.line_ids[0].account_id.id if model.line_ids else suspense_line.account_id.id,
                'partner_id': st_line.partner_id.id or False,
                'currency_id': suspense_line.currency_id.id,
                'amount_currency': total_amount_currency,
                'debit': total_debit,
                'credit': total_credit,
                'reconcile_model_id': model.id,
            })
        
        # Update the move: delete suspense line, add new lines from model
        st_line.with_context(force_delete=True, skip_readonly_check=True).move_id.write({
            'line_ids': [Command.delete(suspense_line.id)] + [Command.create(vals) for vals in new_lines_vals],
        })
        
        return {}