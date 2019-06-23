# -*- coding: utf-8 -*-
from odoo import http

# class HelpanCrmteam(http.Controller):
#     @http.route('/helpan_crmteam/helpan_crmteam/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpan_crmteam/helpan_crmteam/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpan_crmteam.listing', {
#             'root': '/helpan_crmteam/helpan_crmteam',
#             'objects': http.request.env['helpan_crmteam.helpan_crmteam'].search([]),
#         })

#     @http.route('/helpan_crmteam/helpan_crmteam/objects/<model("helpan_crmteam.helpan_crmteam"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpan_crmteam.object', {
#             'object': obj
#         })