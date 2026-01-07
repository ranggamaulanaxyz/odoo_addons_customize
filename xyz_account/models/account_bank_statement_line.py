from odoo import models, fields, api, Command


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    bank_statement_attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'account.bank.statement.line')], string='Bank Statement Attachment')

    def action_open_journal_entry(self):
        self.ensure_one()
        if not self:
            return {}
        result = self.env["ir.actions.act_window"]._for_xml_id(
            "account.action_move_line_form"
        )
        res = self.env.ref("account.view_move_form", False)
        result["views"] = [(res and res.id or False, "form")]
        result["res_id"] = self.move_id.id
        return result

    def set_line_bank_statement_line(self, counterpart_aml_ids=None, payment_aml_ids=None, partner_id=False, **kwargs):
        """
        Reconcile the bank statement line with the provided journal items.
        
        This method replaces the suspense line with a counterpart line matching the 
        account from the selected journal items, then reconciles them.
        
        :param counterpart_aml_ids: List of account.move.line IDs to reconcile with (e.g., invoice lines)
        :param payment_aml_ids: List of payment account.move.line IDs (optional)
        :param partner_id: Partner ID to set on the statement line
        :param kwargs: Additional values (payment_ref, etc.)
        :return: Empty dict for JSON-RPC response compatibility
        """
        self.ensure_one()
        
        # Update partner if provided
        if partner_id:
            self.write({'partner_id': partner_id})
        
        # Update payment_ref if provided
        if kwargs.get('payment_ref'):
            self.write({'payment_ref': kwargs['payment_ref']})
        
        if not counterpart_aml_ids:
            return {}
        
        # Get the counterpart lines to reconcile with
        counterpart_amls = self.env['account.move.line'].browse(counterpart_aml_ids)
        
        if not counterpart_amls:
            return {}
        
        # Get the suspense lines from the statement line's move
        _liquidity_lines, suspense_lines, _other_lines = self._seek_for_lines()
        
        if not suspense_lines:
            return {}
        
        # Get the account from the counterpart lines (e.g., receivable account)
        counterpart_account = counterpart_amls[0].account_id
        
        # Get currency and amounts from the suspense line
        suspense_line = suspense_lines[0]
        
        # Prepare the new counterpart line values using the receivable account
        new_line_vals = {
            'name': self.payment_ref or suspense_line.name,
            'account_id': counterpart_account.id,
            'partner_id': partner_id or self.partner_id.id or counterpart_amls[0].partner_id.id,
            'currency_id': suspense_line.currency_id.id,
            'amount_currency': suspense_line.amount_currency,
            'debit': suspense_line.debit,
            'credit': suspense_line.credit,
        }
        
        # Update the move: delete suspense line, add new counterpart line
        self.with_context(force_delete=True, skip_readonly_check=True).move_id.write({
            'line_ids': [
                Command.delete(suspense_line.id),
                Command.create(new_line_vals),
            ],
        })
        
        # Get the newly created line (the one with the receivable account)
        new_counterpart_line = self.move_id.line_ids.filtered(
            lambda l: l.account_id == counterpart_account and l.id not in counterpart_amls.ids
        )
        
        if new_counterpart_line and counterpart_amls:
            # Now reconcile the new counterpart line with the invoice's receivable line
            (new_counterpart_line + counterpart_amls).reconcile()
        
        return {}

    def set_partner_bank_statement_line(self, partner_id=False, **kwargs):
        """
        Set the partner on the bank statement line.
        
        :param partner_id: Partner ID to set on the statement line
        :param kwargs: Additional values
        :return: Empty dict for JSON-RPC response compatibility
        """
        self.ensure_one()
        
        if partner_id:
            self.write({'partner_id': partner_id})
            # Also update the partner on the move lines
            self.move_id.line_ids.write({'partner_id': partner_id})
        
        return {}

    def delete_reconciled_line(self, line_id=None, **kwargs):
        """
        Delete a reconciled line from the bank statement line's move.
        This removes the specified journal entry line and restores the suspense line if needed.
        
        :param line_id: ID of the account.move.line to delete
        :param kwargs: Additional values
        :return: Empty dict for JSON-RPC response compatibility
        """
        self.ensure_one()
        
        if not line_id:
            return {}
        
        line_to_delete = self.env['account.move.line'].browse(line_id)
        
        if not line_to_delete.exists() or line_to_delete.move_id != self.move_id:
            return {}
        
        # Get the liquidity line to check the expected balance
        _liquidity_lines, _suspense_lines, other_lines = self._seek_for_lines()
        
        # If this is the only other line (besides liquidity), we need to restore the suspense line
        remaining_other_lines = other_lines - line_to_delete
        
        if not remaining_other_lines:
            # No other lines will remain - reset to default suspense configuration
            self.action_undo_reconciliation()
        else:
            # There are still other lines - just remove the reconciliation from this line and delete it
            if line_to_delete.matched_debit_ids or line_to_delete.matched_credit_ids:
                line_to_delete.remove_move_reconcile()
            
            # Get the amount from the line being deleted
            deleted_amount_currency = line_to_delete.amount_currency
            deleted_debit = line_to_delete.debit
            deleted_credit = line_to_delete.credit
            
            # Get the suspense account
            suspense_account = self.journal_id.suspense_account_id
            
            # Create a new suspense line with the deleted line's amounts
            new_suspense_vals = {
                'name': self.payment_ref or 'Suspense',
                'account_id': suspense_account.id,
                'partner_id': self.partner_id.id or False,
                'currency_id': line_to_delete.currency_id.id,
                'amount_currency': deleted_amount_currency,
                'debit': deleted_debit,
                'credit': deleted_credit,
            }
            
            # Delete the line and add the suspense line
            self.with_context(force_delete=True, skip_readonly_check=True).move_id.write({
                'line_ids': [
                    Command.delete(line_to_delete.id),
                    Command.create(new_suspense_vals),
                ],
            })
        
        return {}

    def set_account_bank_statement_line(self, line_id=None, account_id=None, **kwargs):
        """
        Set the account on a specific journal entry line within the statement line's move.
        Used when the user manually selects an account during bank reconciliation.
        
        :param line_id: ID of the account.move.line to update (optional, updates suspense line if not provided)
        :param account_id: ID of the account to set
        :param kwargs: Additional values (name, partner_id, etc.)
        :return: Empty dict for JSON-RPC response compatibility
        """
        self.ensure_one()
        
        if not account_id:
            return {}
        
        account = self.env['account.account'].browse(account_id)
        if not account.exists():
            return {}
        
        if line_id:
            # Update specific line
            line_to_update = self.env['account.move.line'].browse(line_id)
            if not line_to_update.exists() or line_to_update.move_id != self.move_id:
                return {}
        else:
            # Update the suspense line
            _liquidity_lines, suspense_lines, _other_lines = self._seek_for_lines()
            if not suspense_lines:
                return {}
            line_to_update = suspense_lines[0]
        
        # Prepare update values
        update_vals = {'account_id': account_id}
        
        if kwargs.get('name'):
            update_vals['name'] = kwargs['name']
        
        if kwargs.get('partner_id'):
            update_vals['partner_id'] = kwargs['partner_id']
        
        # Update the line
        line_to_update.with_context(skip_readonly_check=True).write(update_vals)
        
        return {}

    def create_document_from_attachment(self, attachment_ids=None, st_line_id=None, **kwargs):
        """
        Create an invoice or bill from an uploaded attachment during bank reconciliation.
        
        :param attachment_ids: List of ir.attachment IDs to process
        :param st_line_id: ID of the statement line (optional if called on a record or in context)
        :param kwargs: Additional values (move_type, partner_id, etc.)
        :return: Dict with created move info for JSON-RPC response compatibility
        """
        # Handle being called on an empty recordset - get statement_line_id from context
        if st_line_id:
            st_line = self.browse(st_line_id)
        elif self:
            st_line = self[0]
        elif self.env.context.get('statement_line_id'):
            st_line = self.browse(self.env.context.get('statement_line_id'))
        else:
            return {'type': 'ir.actions.act_window_close'}
        
        if not attachment_ids:
            return {'type': 'ir.actions.act_window_close'}
        
        attachments = self.env['ir.attachment'].browse(attachment_ids)
        if not attachments.exists():
            return {'type': 'ir.actions.act_window_close'}
        
        # Determine move type based on statement line amount
        if st_line.amount > 0:
            # Incoming payment - likely a customer invoice
            move_type = kwargs.get('move_type', 'out_invoice')
        else:
            # Outgoing payment - likely a vendor bill
            move_type = kwargs.get('move_type', 'in_invoice')
        
        # Create the invoice/bill
        move_vals = {
            'move_type': move_type,
            'partner_id': kwargs.get('partner_id') or st_line.partner_id.id or False,
            'invoice_date': st_line.date,
            'date': st_line.date,
            'journal_id': st_line._get_invoice_journal(move_type).id,
            'company_id': st_line.company_id.id,
            'ref': st_line.payment_ref or '',
        }
        
        move = self.env['account.move'].create(move_vals)
        
        # Attach the files to the invoice
        for attachment in attachments:
            attachment.copy({
                'res_model': 'account.move',
                'res_id': move.id,
            })
        
        # Return an action to open the created invoice/bill
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'target': 'current',
            'context': {
                'from_bank_reco': False,
                'statement_line_id': st_line.id,
                'active_model': 'account.journal',
                'active_id': st_line.journal_id.id,
                'active_ids': [st_line.journal_id.id],
                'default_journal_id': move.journal_id.id,
                'default_move_type': move_type,
                'skip_is_manually_modified': True,
            },
            'views': [[False, 'form']],
            'res_id': move.id,
        }

    def _get_invoice_journal(self, move_type):
        """
        Get the appropriate journal for creating an invoice/bill.
        
        :param move_type: Type of move ('out_invoice', 'in_invoice', etc.)
        :return: account.journal record
        """
        if move_type in ('out_invoice', 'out_refund', 'out_receipt'):
            journal_type = 'sale'
        else:
            journal_type = 'purchase'
        
        return self.env['account.journal'].search([
            ('type', '=', journal_type),
            ('company_id', '=', self.company_id.id),
        ], limit=1)