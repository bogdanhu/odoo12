# -*- coding: utf-8 -*-
from odoo import models, fields, api



# odoo_object Todo sa adaugam o vizualizare
# class purchase_order_line(models.Model):
#     _name = 'purchase.order.line'
#     _inherit = 'purchase.order.line'
#     Dosar = fields.Many2one('helpan_dosar.helpan_dosar', 'Dosar', readonly=False)
#
# class account_invoice_line(models.Model):
#     _name = 'account.invoice.line'
#     _inherit = 'account.invoice.line'
#     Dosar = fields.Many2one('helpan_dosar.helpan_dosar', 'Dosar', readonly=False)
#
# class account_invoice(models.Model):
#     _name = 'account.invoice.line'
#     _inherit = 'account.invoice'
#     Dosar = fields.Many2one('helpan_dosar.helpan_dosar', 'Dosar', readonly=False)
#
#
# class purchase_order_line(models.Model):
#     _inherit = 'purchase.order.line'
#     Dosar = fields.Many2one('helpan_dosar.helpan_dosar', 'Dosar', readonly=False)


#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100



