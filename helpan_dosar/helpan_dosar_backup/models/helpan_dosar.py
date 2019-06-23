# -*- coding: utf-8 -*-

from openerp import api, fields, models, _, osv
import odoo.addons.decimal_precision as dp
import logging
import fdb

_logger = logging.getLogger(__name__)

class helpan_dosar(models.Model):
    _name = 'helpan.dosar'
    _rec_name = "internal_identify"
    _order = 'internal_identify desc'

    name = fields.Char('Name')
    internal_identify = fields.Integer(
        string="Dosar ID", help="Identificare Dosar"
    )
    date_created = fields.Date(string="Created")
    initiator = fields.Char('Initiator')

class purchase_order(models.Model):
    _inherit = 'purchase.order'
    dosar_id = fields.Many2one('helpan.dosar', 'Dosar')

class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.one
    def sincronizeazaEDA(self):
        con = fdb.connect(
            host='192.168.2.163', database='D:\Contabilitate\DataBase\helpan.FDB',
            user='sysdba', password='masterkey'
        )
        cur = con.cursor()
        cur.execute("select lastid from tblcount where name='BXAUTO'")
        result = cur.fetchone()
        newId = result[0] + 1
        cur.execute("insert into BXAUTO(BXID,BXDESCR) VALUES (" + str(newId) + ",'tester')")
        cur.execute("update tblcount set lastid=" + str(newId) + "  WHERE name='BXAUTO'")

        return true

class purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'
    dosar_id = fields.Many2one('helpan.dosar', 'Dosar')

    '''
    # didn't find any fields named "value" or "value2" in purchase.order.line

    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100
    '''

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    dosar_id = fields.Many2one('helpan.dosar', 'Dosar')
    exchange_rate = fields.Float(
        'Curs Euro', digits=dp.get_precision('Account')
    )

class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'
    dosar_id = fields.Many2one('helpan.dosar', 'Dosar')
