# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ToDo(models.Model):
    _name = 'to_do.to_do'
    _description = 'to_do.to_do'

    name = fields.Char(string="Name", required=True)
    user_id = fields.Many2one('res.users', string='To User', required=True)
    model_name = fields.Char(string='Contact', default='res.partner')

    # contact_line = fields.Many2many('res.partner', string='Contact List',
    #                                 domain="[('users_assignations_id', '=', False)]", required=True)
    contact_line = fields.Many2many('res.partner', string='Contact List', required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('assigned', 'Assigned'), ('added_in_pipeline', 'Added in pipeline'),
         ('removed', 'Removed')],
        string='state', default='draft')

    state_level = fields.Integer(default=0)

    _sql_constraints = [
        ('name', 'unique(name)', 'name must be unique !'),
    ]

    # lead_id = fields.Many2one('crm.lead')

    def action_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    def action_assigned(self):
        for rec in self:
            rec.write({'state': 'assigned'})
            for partner in rec.contact_line:
                rec.env['res.partner'].browse(partner.id).write({
                    'users_assignations_id': [(4, rec.user_id.id)]
                })
            rec.user_id.write({'has_assigned': True})

    def action_removed(self):
        for rec in self:
            for partner in rec.contact_line:
                rec.env['res.partner'].browse(partner.id).write({
                    'users_assignations_id': [(3, rec.user_id.id)]
                })
            # remove pipeline too
            # if rec.state == "added_in_pipeline":
            #     crm_lead = rec.env['crm.lead'].search([('name', '=', rec.name), ('is_batch', '=', True)])
            #     for crm in crm_lead:
            #         crm.unlink()
            rec.write({'state': 'removed'})
            rec.user_id.write({'has_assigned': False})

    def action_create_lead(self):
        for rec in self:
            rec.sudo().write({'state': 'added_in_pipeline'})
            for partner in rec.contact_line:
                rec.env['crm.lead'].sudo().create({
                    'name': rec.name,
                    'partner_id': partner.id,
                    'type': 'opportunity',
                    'is_batch': True,
                })

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
        self_contact_line = self.contact_line
        for c in self.contact_line:
            self_contact.append(c.id)
        if 'contact_line' in vals and self.state == "assigned":
            if vals.get('contact_line')[0][2]:
                # get the difference len of self value and vals value
                diff = self.difference(vals.get('contact_line')[0][2], self_contact)
                if diff:
                    # define the action user: delete or add contact line
                    action_type = self.action_type(vals.get('contact_line')[0][2], self_contact)
                    if action_type == "del or add":
                        # user add contact line
                        if len(self_contact) < len(vals.get('contact_line')[0][2]):
                            for contact_del_id in diff:
                                self.env['res.partner'].browse(contact_del_id).write({
                                    'users_assignations_id': [(4, self.user_id.id)]
                                })
                        # user delete contact line
                        else:
                            for contact_del_id in diff:
                                self.env['res.partner'].browse(contact_del_id).write({
                                    'users_assignations_id': [(3, self.user_id.id)]
                                })
                    # user change all contact line
                    if action_type == "change":
                        for contact_id in self_contact:
                            self.env['res.partner'].browse(contact_id).write({
                                'users_assignations_id': [(3, self.user_id.id)]
                            })
                        for contact_id in vals.get('contact_line')[0][2]:
                            self.env['res.partner'].browse(contact_id).write({
                                'users_assignations_id': [(4, self.user_id.id)]
                            })
                for vcl in vals.get('contact_line')[0][2]:
                    self.env['res.partner'].browse(vcl).write({
                        'users_assignations_id': [(4, self.user_id.id)]
                    })
            else:
                for sc in self_contact_line:
                    self.env['res.partner'].browse(sc.id).write({
                        'users_assignations_id': [(3, self.user_id.id)]
                    })
        # change crm name
        if 'name' in vals and vals.get('name') and self.state == "added_in_pipeline":
            lead = self.env['crm.lead'].search([('name', '=', self.name), ('is_batch', '=', True)])
            for l in lead:
                l.write({'name': vals.get('name')})

        res = super(ToDo, self).write(vals)
        return res
