# -*- coding: utf-8 -*-

#
#    odoo extensions
#
#    © 2017-now Josef Kaser (<http://www.pragmasoft.de>).
#
#   See the LICENSE file in the toplevel directory for copyright
#   and license details.
#
import math

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare

import logging

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    _name = _inherit

    ps_pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')

    @api.multi
    @api.onchange('partner_id')
    def _set_currency(self):
        for invoice in self:
            if invoice.partner_id:
                if invoice.partner_id.property_product_pricelist:
                    invoice.currency_id = invoice.partner_id.property_product_pricelist.currency_id
                elif invoice.partner_id.country_id and invoice.partner_id.country_id.currency_id:
                    invoice.currency_id = invoice.partner_id.country_id.currency_id
                else:
                    invoice.currency_id = self.env.user.company_id.currency_id

            if invoice.partner_id and invoice.partner_id.property_product_pricelist:
                invoice.ps_pricelist_id = invoice.partner_id.property_product_pricelist

            if invoice.invoice_line_ids:
                self._calculate_invoice_lines(invoice.invoice_line_ids)

    @api.multi
    @api.onchange('ps_pricelist_id')
    def _set_pricelist(self):
        for invoice in self:
            if invoice.ps_pricelist_id:
                invoice.currency_id = invoice.ps_pricelist_id.currency_id

            if invoice.invoice_line_ids:
                self._calculate_invoice_lines(invoice.invoice_line_ids)

    @api.multi
    @api.onchange('currency_id')
    def _check_currency_id(self):
        for invoice in self:
            if not (invoice.currency_id):
                if invoice.ps_pricelist_id:
                    if invoice.currency_id != invoice.ps_pricelist_id.currency_id:
                        raise ValidationError(
                            _('The selected currency %s does not match the currency %s of the pricelist.') % (
                                invoice.currency_id.name, invoice.ps_pricelist_id.currency_id.name))
            else:
                _logger.info("s-a schimbat valuta")

                if invoice.invoice_line_ids:
                    if invoice.ps_pricelist_id.currency_id.name == "EUR" and invoice.currency_id.name=="RON":
                        self._calculate_invoice_lines(invoice.invoice_line_ids)
                    else:
                        self._calculate_invoice_linesFaraCurs(invoice.invoice_line_ids)

    def _calculate_invoice_lines(self, invoice_lines):
        for invoice_line in invoice_lines:
            if invoice_line.invoice_id.ps_pricelist_id:
                invoice_line.price_unit = invoice_line.invoice_id.ps_pricelist_id.get_product_price(
                    invoice_line.product_id, invoice_line.quantity, invoice_line.invoice_id.partner_id,
                    uom_id=invoice_line.uom_id.id) * invoice_line.invoice_id.ExchangeRateEurRON
        _logger.info("Am schimbat valoarea")

    # momentan nu ma descurc prea bine
    def _calculate_invoice_linesFaraCurs(self, invoice_lines):
        for invoice_line in invoice_lines:
            if invoice_line.invoice_id.ps_pricelist_id:
                invoice_line.price_unit = invoice_line.invoice_id.ps_pricelist_id.get_product_price(
                    invoice_line.product_id, invoice_line.quantity, invoice_line.invoice_id.partner_id,
                    uom_id=invoice_line.uom_id.id)
                s=str(invoice_line.name)
                indexValoare = s.find("Valoare in EUR")
                if indexValoare>0:
                    self.invoice_line=s[:indexValoare]

        _logger.info("Am pus valoarea nominala")


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    _name = _inherit

    def set_taxes(self):
        if self.invoice_id.type in ('out_invoice', 'out_refund'):
            taxes = self.product_id.taxes_id or self.account_id.tax_ids
        else:
            taxes = self.product_id.supplier_taxes_id or self.account_id.tax_ids

        # Keep only taxes of the company
        company_id = self.company_id or self.env.user.company_id
        taxes = taxes.filtered(lambda r: r.company_id == company_id)

        self.invoice_line_tax_ids = fp_taxes = self.invoice_id.fiscal_position_id.map_tax(taxes, self.product_id,
                                                                                          self.invoice_id.partner_id)

    def compute_price(self):
        self._compute_price()

    def compute_amount_currency(self, from_currency_id, to_currency_id):
        from_currency = self.env['res.currency'].browse(from_currency_id)
        to_currency = self.env['res.currency'].browse(to_currency_id)

        self.amount_currency = self.price * from_currency._get_conversion_rate(self, to_currency)

    @api.multi
    @api.onchange('product_id', 'quantity', 'uom_id')
    def _calculate_price(self):
        for invoice_line in self:
            if invoice_line.product_id:
                if invoice_line.invoice_id.ps_pricelist_id:

                    invoice_line.price_unit = invoice_line.invoice_id.ps_pricelist_id.get_product_price(
                        invoice_line.product_id, invoice_line.quantity, invoice_line.invoice_id.partner_id,
                        uom_id=invoice_line.uom_id.id)

                    if invoice_line.invoice_id.ps_pricelist_id.currency_id.name == "EUR" and invoice_line.invoice_id.currency_id.name == "RON":
                        _logger.info("Calculez valorile convertite\n")
                        _logger.critical(invoice_line.invoice_id.ExchangeRateEurRON)

                        _logger.info(self.name)
                        invoice_line.name=str(self.name)+str("\nValoare in EUR: ")+str(round(invoice_line.price_unit,4))+str('\u20ac') # aici trebuie sa scriu cat era
                        invoice_line.price_unit = invoice_line.price_unit * invoice_line.invoice_id.ExchangeRateEurRON# valoarea in EUR
                    _logger.info("Am schimbat valoareaX")
