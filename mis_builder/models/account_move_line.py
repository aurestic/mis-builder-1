from odoo import api, models, fields


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

    @api.depends('account_id', 'account_id.group_id')
    def _compute_account_group(self):
        for record in self:
            record.account_group_id = record.account_id.pargroup_ident_id

    @api.depends('account_id.root_id', 'account_id.root_id.parent_id')
    def _compute_account_root_parent(self):
        for record in self:
            record.account_root_parent_id = record.account_id.root_id.parent_id
