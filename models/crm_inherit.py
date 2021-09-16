# -*- coding: utf-8 -*-


from odoo import models, fields, api


class CrmInherit(models.Model):
    _inherit = 'crm.lead'

    is_batch = fields.Boolean()

    # def action_menu_pipeline(self):
    #     user_has_groups_agent = self.user_has_groups('to_do.group_user_agents')
    #     if user_has_groups_agent:
    #         domain = ['&', '|', ('partner_id.users_assignations_id.id', '=', self.env.user.id), ('type', '=', 'lead'),
    #                   ('type', '=', False)]
    #     else:
    #         domain = ['|', ('type', '=', 'lead'), ('type', '=', False)]
    #     return {
    #         'name': 'Pipeline',
    #         'domain': domain,
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'crm.lead',
    #         'view_mode': 'kanban,tree,graph,pivot,calendar,form,activity',
    #         'search_view_id': self.env.ref('crm.view_crm_case_leads_filter').id,
    #         'context': self.env.context
    #     }
