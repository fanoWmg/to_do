# -*- coding: utf-8 -*-

from odoo import models, fields, api


class UsersInherit(models.Model):
    _inherit = 'res.users'

    has_assigned = fields.Boolean()