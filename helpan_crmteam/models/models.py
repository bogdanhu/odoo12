# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class crm_team(models.Model):
    _inherit = 'crm.team'
    type='sale'
    JurnalFacturiClienti= fields.Many2one('account.journal', domain="[('type','=','sale')]",string='Jurnal alocat facturilor clientilor acestei echipe',
                                  help="Pentru automatizare facturilor")
    JurnalFacturiFurnizori = fields.Many2one('account.journal', domain="[('type','=','purchase')]",string='Jurnal alocat facturilor furnizorilor acestei echipe',
                                  help="Pentru automatizare facturilor")

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _default_journal_type(self):
        _logger.debug('\n\n\nJurnalizam')
        useri = self.env["res.users"]
        context = self._context
        actiune = context.get('action')
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        _logger.debug('\n\n\nMda'+str(actiune))
        # if actiune == 371:
        #     if (user.team_id.JurnalFacturiClienti is None):
        #         return 14
        #     else:
        #         return user.team_id.JurnalFacturiClienti
        # else:
        #     if actiune==372:
        #         if (user.team_id.JurnalFacturiFurnizori is None):
        #             return 22
        #         else:
        #             return user.team_id.JurnalFacturiFurnizori
    #TODO: nu merge :(
    journal_id=fields.Many2one('account.journal',context="{'user_team_id': 3}",default=_default_journal_type)



class ProductTemplate(models.Model):
    _inherit = 'product.template'
    #TODO: sa aloc in facturi tipul de jurnal; am de facut o

       # return 2
    @api.model
    def _default_product_type(self):
        useri = self.env["res.users"]
        context = self._context

        current_uid = context.get('uid')

        user = self.env['res.users'].browse(current_uid)
        return user.team_id
    team_id = fields.Many2one('crm.team', string='Echipa de vanzari',  context="{'user_team_id': 3}",default=_default_product_type)
    #barcode=  fields.Char(default='111111')
    type=fields.Selection(default='product')


    def _get_team_id(self):

        user = self.pool.get('res.users').search('id','=',self._context.get('uid'))
        return user.team_id

    # @api.model
    # def default_get(self, fields):
    #     rec = super(ProductTemplate, self).default_get(fields)
    #     _logger.debug('\nSupraalocam')
    #     useri = self.env["res.users"]
    #     context = self._context
    #
    #     current_uid = context.get('uid')
    #
    #     user = self.env['res.users'].browse(current_uid)
    #     rec['user_team_id']= user
    #     return rec

class ResUsers(models.Model):
    _inherit = 'res.users'
    team_id = fields.Many2one('crm.team', string='Echipa de vanzari')
# class helpan_crmteam(models.Model):
#     _name = 'helpan_crmteam.helpan_crmteam'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100