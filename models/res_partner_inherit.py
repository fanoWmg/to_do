# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RepartnerInherit(models.Model):
    _inherit = 'res.partner'

    users_assignations_id = fields.Many2many('res.users', 'partner_id', 'user_id', 'res_partner_user_assign_rel',
                                             string='User Assignation')

    def action_menu_contact(self):
        user_has_groups_agent = self.user_has_groups('to_do.group_user_agents')
        if user_has_groups_agent:
            domain = [('users_assignations_id', 'child_of', [self.env.user.id])]
        else:
            domain = [(1, "=", 1)]
        return {
            'name': 'Contacts',
            'domain': domain,
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'kanban,tree,form,activity',
            'context': {'default_is_company': True},
        }

