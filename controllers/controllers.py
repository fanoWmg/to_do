# -*- coding: utf-8 -*-
# from odoo import http


# class ToDo(http.Controller):
#     @http.route('/to_do/to_do/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/to_do/to_do/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('to_do.listing', {
#             'root': '/to_do/to_do',
#             'objects': http.request.env['to_do.to_do'].search([]),
#         })

#     @http.route('/to_do/to_do/objects/<model("to_do.to_do"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('to_do.object', {
#             'object': obj
#         })
