# -*- coding: utf-8 -*-
from odoo import http
#from openerp.addons.web import http as http

class HelpanDosar(http.Controller):
     @http.route('/helpan_dosar/helpan_dosar/', auth='public')
     def index(self, **kw):
         return "Hello, world"

#     @http.route('/helpan_dosar/helpan_dosar/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpan_dosar.listing', {
#             'root': '/helpan_dosar/helpan_dosar',
#             'objects': http.request.env['helpan_dosar.helpan_dosar'].search([]),
#         })

#     @http.route('/helpan_dosar/helpan_dosar/objects/<model("helpan_dosar.helpan_dosar"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpan_dosar.object', {
#             'object': obj
#         })