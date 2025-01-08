from odoo import api, models, fields
from odoo.tools.sql import column_exists, create_column


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    account_group_id = fields.Many2one(
        'account.group',
        store=True,
        readonly=True,
        compute='_compute_account_group'
    )
    account_root_parent_id = fields.Many2one(
        'account.root',
        store=True,
        readonly=True,
        compute='_compute_account_root_parent'
    )

    def _auto_init(self):
        if not column_exists(self.env.cr, self._table, 'account_group_id'):
            create_column(self.env.cr, self._table, 'account_group_id', 'int4')
            self.env.cr.execute("""
                UPDATE account_move_line line
                SET account_group_id = account.group_id
                FROM account_account account
                WHERE account.id = line.account_id
            """)
        if not column_exists(self.env.cr, self._table, 'account_root_parent_id'):
            create_column(self.env.cr, self._table, 'account_root_parent_id', 'int4')
            self.env.cr.execute("""
                UPDATE account_move_line line
                SET account_root_parent_id = account_root.parent_id
                FROM account_root
                WHERE account_root.id = line.account_root_id
            """)
        return super()._auto_init()

    @api.depends('account_id', 'account_id.group_id')
    def _compute_account_group(self):
        for record in self:
            record.account_group_id = record.account_id.group_id

    @api.depends('account_id.root_id', 'account_id.root_id.parent_id')
    def _compute_account_root_parent(self):
        for record in self:
            record.account_root_parent_id = record.account_id.root_id.parent_id
