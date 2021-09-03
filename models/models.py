# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ToDo(models.Model):
    _name = 'to_do.to_do'
    _description = 'to_do.to_do'

    name = fields.Char(string="Name", required=True)
    user_id = fields.Many2one('res.users', string='To User', required=True, domain="[('has_assigned', '=', False)]")
    model_name = fields.Char(string='Contact', default='res.partner')

    contact_line = fields.Many2many('res.partner', string='Contact List',
                                    domain="[('users_assignations_id', '=', False)]", required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('assigned', 'Assigned'), ('executed', 'Executed'), ('removed', 'Removed')],
        string='state', default='draft')

    state_level = fields.Integer(default=0)

    # lead_id = fields.Many2one('crm.lead')

    def action_draft(self):
        for rec in self:
            rec.write({'state': 'draft', 'state_level': 0})

    def action_assigned(self):
        for rec in self:
            rec.write({'state': 'assigned', 'state_level': 1})
            for partner in rec.contact_line:
                rec.env['res.partner'].browse(partner.id).write({
                    'users_assignations_id': rec.user_id
                })
            rec.user_id.write({'has_assigned': True})

    def action_removed(self):
        for rec in self:
            for partner in rec.contact_line:
                rec.env['res.partner'].browse(partner.id).write({
                    'users_assignations_id': False
                })
            rec.write({'state': 'removed'})
            rec.user_id.write({'has_assigned': False})

    def action_executed(self):
        for rec in self:
            rec.write({'state': 'executed', 'state_level': 3})

    # @api.onchange('model_id')
    # def _onchange_model_id(self):
    #     if self.model_id:
    #         self.model_name = self.model_id.model
    #     else:
    #         self.model_name = False

    def difference(self, list1, list2):
        list_dif = [i for i in list1 + list2 if i not in list1 or i not in list2]
        return list_dif

    def action_type(self, list1, list2):
        action = ""
        if len(list1) <= len(list2):
            for i in list1:
                if i not in list2:
                    action = "change"
                else:
                    action = "del or add"
                    break
        else:
            for i in list2:
                if i not in list1:
                    action = "change"
                else:
                    action = "del or add"
                    break
        return action

    def write(self, vals):
        self_contact = []
        if 'contact_line' in vals and vals.get('contact_line')[0][2]:
            vals_contact = vals.get('contact_line')[0][2]
            for c in self.contact_line:
                self_contact.append(c.id)
            diff = self.difference(vals_contact, self_contact)
            if diff:
                action_type = self.action_type(vals_contact, self_contact)
                if action_type == "del or add":
                    # user add contact line
                    if len(self_contact) < len(vals_contact):
                        for contact_del_id in diff:
                            self.env['res.partner'].browse(contact_del_id).write({
                                'users_assignations_id': self.user_id.id
                            })
                    # user delete contact line
                    else:
                        for contact_del_id in diff:
                            self.env['res.partner'].browse(contact_del_id).write({
                                'users_assignations_id': False
                            })
                if action_type == "change":
                    for contact_id in self_contact:
                        self.env['res.partner'].browse(contact_id).write({
                            'users_assignations_id': False
                        })
                    for contact_id in vals_contact:
                        self.env['res.partner'].browse(contact_id).write({
                            'users_assignations_id': self.user_id.id
                        })
            else:
                print("empty diff")
                pass
        if 'contact_line' in vals and not vals.get('contact_line')[0][2]:
            for contact in self.env['res.partner'].search([('users_assignations_id', '=', self.user_id.id)]):
                contact.write({'users_assignations_id': False})
            self.user_id.sudo().write({'has_assigned': False})

        res = super(ToDo, self).write(vals)
        return res


class RepartnerInherit(models.Model):
    _inherit = 'res.partner'

    users_assignations_id = fields.Many2one('res.users', 'partner_id')


class UsersInherit(models.Model):
    _inherit = 'res.users'

    has_assigned = fields.Boolean()
