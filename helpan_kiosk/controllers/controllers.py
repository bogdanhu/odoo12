# -*- coding: utf-8 -*-
from odoo import http

# class HelpanKiosk(http.Controller):
#     @http.route('/helpan_kiosk', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

class HelpanKiosk(http.Controller):
    @http.route('/helpan_kiosk', type='http', auth='public', website=True)
    def render_example_page(self):
        dosare = http.request.env['helpan.dosar'].sudo().search([])
        return http.request.render('helpan_kiosk.bogdan', {
            'dosare' : dosare,
        })
        #return "Hello, world"
        #return http.request.render('create_webpage_demo.example_page', {})

    @http.route('/helpan_kiosk/detail', type='http', auth='public', website=True)
    def navigate_to_detail_page(self) :
        # This will get all company details (in case of multicompany this are multiple records)
        companies = http.request.env['res.company'].sudo().search([])
        return http.request.render('create_webpage_demo.detail_page', {
            # pass company details to the webpage in a variable
            'companies' : companies})



#     @http.route('/helpan_kiosk/helpan_kiosk/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpan_kiosk.listing', {
#             'root': '/helpan_kiosk/helpan_kiosk',
#             'objects': http.request.env['helpan_kiosk.helpan_kiosk'].search([]),
#         })

#     @http.route('/helpan_kiosk/helpan_kiosk/objects/<model("helpan_kiosk.helpan_kiosk"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpan_kiosk.object', {
#             'object': obj
#         })