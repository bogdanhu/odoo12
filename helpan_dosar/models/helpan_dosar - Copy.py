# -*- coding: utf-8 -*-
import sys
sys.path.append("pycharm-debug-py3k.egg")
import pydevd
pydevd.settrace('192.168.0.104', port=12345, stdoutToServer=True, stderrToServer=True)

from openerp import api, fields, models, osv
from odoo.exceptions import UserError  # pentru UserError
import odoo.addons.decimal_precision as dp
import logging
import fdb
import time
import datetime
## Conectare la MSSQL
import pyodbc
import requests
import sqlalchemy
import fdb
from datetime import datetime

from sqlalchemy import create_engine, inspect
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy import exc

from urllib.parse import quote_plus

import importlib
import sys

importlib.reload(sys)
# sys.setdefaultencoding('utf-8')
# ISO-8859-16
# utf-8
# latin-1
_logger = logging.getLogger(__name__)

from sqlalchemy import (MetaData, Table, Column, Integer, String, Date, Float, select, literal, and_, exists)

from sqlalchemy import create_engine

#TODO - iau din odoo produsul si sa il pun in EDA
#practic iau numele si codul si caut asa
#daca ii gasesc codul si in EDA il notific si il adaug
#daca nu il gassec , ii pun codul default pentru echipa si il adaug
engineEDA = create_engine('firebird+fdb://sysdba:masterkey@192.168.2.163:3050/D:\Contabilitate\DataBase\helpan.FDB')
metadataEDA = MetaData()
class ProdusEDA:
    def __init__(self,bxcod):
        _logger.info(str(bxcod))
        BXPARTTable = Table("BXPART", metadataEDA, autoload=True, autoload_with=engineEDA)
        if(bxcod!=False):
            BXCOD = bxcod
        else:
            BXCOD=""
        select_stmt = BXPARTTable.select().where(BXPARTTable.c.bxcod == BXCOD).order_by(BXPARTTable.c.bxcod.desc()).limit(1)
        _logger.info(select_stmt)
        rezultat = engineEDA.execute(select_stmt).fetchone()
        if(rezultat!=None):
            self.EDA_BXID = rezultat[0]
            self.EDA_BXCOD = rezultat[1]
            self.EDA_BXNUME = rezultat[2]
            self.EDA_BXUM_ID = rezultat[3]
            self.EDA_GRUPA_ID = rezultat[4]
            self.EDA_BXCOTATVAIMPLICIT_ID=rezultat[5]
            self.EDA_BXCONTIMP_ID_V=rezultat[8]
            _logger.info("Next step")
        else:
            self.EDA_BXID=46
            self.EDA_BXCOD=BXCOD
            self.EDA_BXNUME='Marfa'
            self.EDA_BXUM_ID=1
            self.EDA_BXCOTATVAIMPLICIT_ID=4
            self.EDA_BXCONTIMP_ID_V=142

            #daca are cod in Odoo il adaugam in SWAN
            # daca nu il adaugam ca marfa - ATENTIE - in functie de echipa ?
            #ideal ar fi sa ii pun pe pagina de echipa produs standard
            #45- avans - AVANS
            #46 - marfa - MARF
            #107 - transport - TRANSP
            #107,45179,46
            _logger.info("Eroare 11: Nu gasesc codul")




class ResCurrency(models.Model):
    _inherit = 'res.currency'
    swanBXVALUTAID = fields.Integer(string="ID Valuta din EDA",required=False,help="Ce ID avem in EDA; 1 - LEI ; 2-EURO ",default=1)

class dosar(models.Model):
    _name = 'dosar'
    _rec_name = "internal_identify"
    _order = 'internal_identify desc'
    _inherit = 'mail.thread'
    name = fields.Char('Name')

    internal_identify = fields.Integer( string="Dosar ID", help="Identificare Dosar")
    date_created = fields.Date(string="Created")
    initiator = fields.Char('Initiatorul')
    facturi_ids = fields.One2many('account.invoice', 'dosar_id') #sa am toate facturile aferente dosarului
    ResponsabilTehnic=fields.Many2one('hr.employee','Responsabil Tehnico Comercial',help="Cine are responsabilitatea acestui dosar / sunt cu functia de INGINER PROIECTANT")
    facturat=fields.Float(string='Valoare Facturata fara TVA',compute='_get_sum_invoices')
    platit=fields.Float(string='Valoare Incasata CU TVA',compute='_get_sum_payments')
    denumire_completa_dosar = fields.Char(string='Denumire completa', compute='_set_complete_name')
#total Factura Clienti
#total Factura Furnizori
#total Rezultat
    @api.one
    def _get_sum_invoices(self):
        facturare = self.env['account.invoice'].search([('dosar_id', '=', self.id)])
        _logger.info('Caut facturi in dosarul : '+str(self.internal_identify))
        self.facturat=sum(item.amount_untaxed for item in facturare)

    @api.one
    def _set_complete_name(self):
        if(type(self.internal_identify)!=int):
            self.internal_identify=0
        if (type(self.name) != str):
            self.name="NONAME"
        self.denumire_completa_dosar = str(self.internal_identify) + " - " + self.name

    @api.one
    def _get_sum_payments(self):
        facturare = self.env['account.invoice'].search([('dosar_id', '=', self.id)])
        _logger.info('Caut facturi platite in dosarul : ' + str(self.internal_identify))
        for item in facturare:
            self.platit+=(item.amount_total_signed-item.residual)
    def trimiteMail(self):
        template = self.env.ref('mail_template_demo.example_email_template')
        # You can also find the e-mail template like this:
        # template = self.env['ir.model.data'].get_object('mail_template_demo', 'example_email_template')

        # Send out the e-mail template to the user
        self.env['mail.template'].browse(template.id).send_mail(14)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    contActiveDirectory = fields.Char(string="Active Directory", required=False, help="Cont de logare pe windows")
    dosare_ids= fields.One2many('dosar', 'ResponsabilTehnic')
    facturat = fields.Float(string='Valoare Facturata fara TVA', compute='_get_sum_invoices')

    # total Factura Clienti
    # total Factura Furnizori
    # total Rezultat
    @api.one
    def _get_sum_invoices(self):
        dosare = self.env['dosar'].search([('ResponsabilTehnic', '=', self.id)])
        TotalFacturat=0
        for dosar in dosare:
            facturi = self.env['account.invoice'].search([('dosar_id', '=', dosar.id)])
            _logger.info('Facturi '+str(len(facturi)))
            for factura in facturi:
                TotalFacturat=TotalFacturat+factura.amount_untaxed
        self.facturat = TotalFacturat

   # facturi_ids = fields.Reference([('account.invoice', 'Factura'),('helpan.dosar','Dosar')],'Category',)  # sa am toate facturile aferente dosarului
#SELECT facturi_IDS FROM dosar,invoice,employee WHERE invoice.dosar_id=dosar_id AND dosar_responsabil=employee_id

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    dosar_id = fields.Many2one('dosar', 'Dosar')
    team_id = fields.Many2one('crm.team', 'Echipa')

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    dosar_id = fields.Many2one('dosar', 'Dosar')
    team_id = fields.Many2one('crm.team', 'Echipa')




class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    dosar_id = fields.Many2one('dosar', 'Dosar')

    '''
    # didn't find any fields named "value" or "value2" in purchase.order.line

    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100
    '''


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    #_name= _inherit_dosar
    swanFacturaID = fields.Integer(string="ID Factura din EDA")
    esteSincronizatEDA = fields.Boolean(string="Este sincronizat deja?")
    dosar_id = fields.Many2one('dosar', 'Dosar')

    # curs=round(1/model('').browse(1).rate,4)

    def setCurrency(self):
        currencies = self.env["res.currency"]
        id_needed = currencies.search([('name', '=', 'EUR')]).rate
        # round(1/model('res.currency').browse(1).rate,4)
        CursBNR = round(1 / id_needed, 4)
        CursBNR = CursBNR
        _logger.info(CursBNR)
        return CursBNR

    ExchangeRateEurRON = fields.Float('Curs Euro', digits=dp.get_precision('Account'), default=setCurrency)

    @api.one
    def adaugaComentariuDaedalus(self, server, database):
        connection_string = "DRIVER={ODBC Driver 13 for SQL Server};TimeOut=2;Database=" + database + ";SERVER=" + \
                            server + ";UID=bogdan;PWD=HELPAN123$;TIMEOUT=2"
        connection_string = quote_plus(connection_string)
        connection_string = "mssql+pyodbc:///?odbc_connect=%s" % connection_string
        _logger.info(connection_string)

        try:
            engine = sqlalchemy.create_engine(connection_string)
            _logger.info('\nRunning: ' + connection_string)
            from sqlalchemy.engine.reflection import Inspector
            sql = 'UPDATE DOSARE set Valoare = {0} WHERE DosarID= {1}'.format(str(self.amount_untaxed), str(
                self.dosar_id.internal_identify))
            _logger.info('\nRunning: ' + sql)
            result = engine.execute(sql)
            cur = 1

            now = datetime.now()  # timezone-aware datetime.utcnow()  ola
            FORMAT = '%Y-%m-%dT'
            engine = sqlalchemy.create_engine(connection_string)
            sql = "INSERT INTO Comentarii (Continut,Utilizator,DosarID,Data) VALUES (\'factura {0} cu  valoarea {1} lei " \
                  "fara TVA" \
                  "\'," \
                  "\'{2}\',{3},\'{4}\')".format(
                str(self.number), str(self.amount_untaxed), str(self.user_id.name), str(
                    self.dosar_id.internal_identify), now)
            _logger.info('\nRunning: ' + sql)
            result = engine.execute(sql)

        except IndexError:
            cur = -2
        # except exc.SQLAlchemyError as ex:
        #    _logger.info(ex.__class__)
        #    cur = -3
        _logger.info('\nReturnare comanda: ' + str(cur))
        return cur
    @api.one
    def adaugaFacturainEDA(self,cur,con,numarFactura,serieFactura,BXCONT_ID,BXREC_TYPE,BXVALUTA_ID,BXVALUTA_CURS):
        cur.execute("select lastid from tblcount where name='BXIESIRE'")
        result = cur.fetchone()
        BXID = result[0] + 1
        # BXCONT_ID - 246 - DRAGOS;  221 - HP
        BXIESIRETIPDOC_ID = 4  # 4 HP ; 5 HEV
        BXCUSTOMER_ID = self.partner_id.swan_ID  # de afisat daca e partner_id sau partner_id.id
        BXDOC_NO = numarFactura
        BXDOC_DATE = datetime.strptime(self.date_invoice, '%Y-%m-%d').strftime('%d.%m.%Y %H:%M:%S')
        # 2018-08-10
        # '2018-07-11' does not match format '%Y-%m-%d'
        # '20.10.2011 10:10:10'

        BXGAMOUNT = self.amount_total  # test
        BXVALFTVA = self.amount_untaxed  # test
        BXVALTVA = self.amount_tax  # test
        BXLAMOUNT = self.amount_total  # test
        BXSETTLED_VALUE = self.amount_total
        # timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # BXDATASCADENTA = time.mktime(datetime.datetime.strptime(self.date_due, '%Y-%m-%d').timetuple())
        # BXDATASCADENTA = datetime.datetime.strptime(self.date_due, '%d.%m.%Y')
        BXDATASCADENTA = datetime.strptime(self.date_due, '%Y-%m-%d').strftime('%d.%m.%Y %H:%M:%S')
        BXVATCONT_ID = 72  # asa e in BD
        BXUNITATE_ID = 0  # asa era in BD
        BXSURSA_ID = 1  # asa era in BD
        BXVALCASA = 0  # asa era
        BXSOLD = self.amount_total
        BXSOLDINT = 1  # ce draci o fi
        BXUNITATE_ID = 0
        BXSURSA_ID = 1  # ce inseamna?

        BXVATCONT_ID = 72  # la toate
        BXSOLD = self.amount_total
        BXSOLDINT = 1
        BXSERIA = serieFactura
        interogare = "INSERT INTO BXIESIRE (BXID,BXCONT_ID,BXREC_TYPE,BXIESIRETIPDOC_ID,BXCUSTOMER_ID,BXDOC_NO," \
                     "BXDOC_DATE,BXVALUTA_ID,BXVALUTA_CURS,BXGAMOUNT,BXVALFTVA,BXVALTVA,BXLAMOUNT,BXSETTLED_VALUE," \
                     "BXDATASCADENTA,BXVATCONT_ID,BXUNITATE_ID,BXSURSA_ID,BXVALCASA,BXSOLD,BXSOLDINT,BXSERIA) VALUES(" \
                     + str(BXID) + "," + str(BXCONT_ID) + "," + str(BXREC_TYPE) + "," + str(
            BXIESIRETIPDOC_ID) + "," + str(BXCUSTOMER_ID) + "," + str(BXDOC_NO) + ",'" + str(BXDOC_DATE) + "'," + str(
            BXVALUTA_ID) + "," + str(BXVALUTA_CURS) + "," + str(BXGAMOUNT) + "," + str(BXVALFTVA) + "," + str(
            BXVALFTVA) + "," + str(BXLAMOUNT) + "," + str(BXSETTLED_VALUE) + ",'" + str(BXDATASCADENTA) + "'," + str(
            BXVATCONT_ID) + "," + str(BXUNITATE_ID) + "," + str(BXSURSA_ID) + "," + str(BXVALCASA) + "," + str(
            BXSOLD) + "," + str(BXSOLDINT) + ",'" + str(BXSERIA) + "')"

        try:
            _logger.info(interogare)
            cur.execute(interogare)
            _logger.info('\nInserare cu succes')
            self.esteSincronizatEDA = True
        except:
            raise UserError('Nu pot sa inserez factura')
            return

        try:
            interogare = "update tblcount set lastid=" + str(BXID) + "  WHERE name='BXIESIRE'"
            _logger.info(interogare)
            cur.execute(interogare)
        except:
            raise UserError('Nu pot sa actualizez starea ID-urilor')
        con.commit()  # TODO De mutat mai jos
        #raise UserError("nu avem implementare - TODO\n" + str(BXCUSTOMER_ID) + " " + str(            self.partner_id.id) + "" + self.date_due + " " + str(BXDATASCADENTA))
    @api.one
    def sincronizeazaEDA(self, context=None):
        if (self.dosar_id.internal_identify > 0):
            self.adaugaComentariuDaedalus("192.168.2.49", "Metal")
        else:
            UserWarning('Nu avem Dosar alocat')
        # teoretic face asa   12.07.2018 // 27.01.2019 / 03.03.2019
        # 0. verifica daca e sincronizat documentul (daca exista) - Partial
        # 1. verifica daca clientul e sincronizat (NOK - trebuie sa verific daca e persoana fizica si daca da, daca e reprezentantul unei firme!)
        # 2. adauga liniile de produs - 03.03.2019 - aici sunt
        # 3. adauga totalul la factura
        # 4. adauga valorile la swanFacturaID si bifeaza este SincronizatEDA
        # ce facem daca are factura straina?
        # cum dam revert?
        res = {}
        update = False

        # Pasul 0
        if (self.esteSincronizatEDA == True):
            _logger.info('Baza de date este sincronizata')
            res = {'warning': {'title': _('Warning'), 'message': _('Este deja sincronizat' + str(self.name))}}
            return {
                'warning': {'title': _('Error'), 'message': _('Error message'), },
            }
        if res:
            return res
        con = fdb.connect(
            host='192.168.2.163', database='D:\Contabilitate\DataBase\helpan.FDB',
            user='sysdba', password='masterkey'
        )
        cur = con.cursor()
        _logger.info("Verificam daca avem inregistrari\n");
        # PASUL 0.A - De verificat dupa documentul din Odoo in SWAN
        # PASUL 1
        if (not ((self.state == "open") or (self.state == "paid"))):
            raise UserError(('Nu putem sincroniza facturi decat deschise sau platite'))
            return
        serieFactura, numarFactura = self.number.split("-")
        if (not (self.partner_id.esteSincronizatEDA)):
            raise UserError( 'Userul nu e sincronizat' + str(serieFactura) + " " + str(numarFactura))
            return
        BXCONT_ID = self.team_id.ContFacturi.swanContID  # 221 - HP sau 246 - Dragos
        BXREC_TYPE = 2  # nu stiu ce inseamna
        BXVALUTA_CURS = self.ExchangeRateEurRON
        BXVAT_ID=4 # probabil e pentru 19 %
        BXCONTGEST_ID=1 #pentru SM ; 4 pentru Utilaje

        BXVALUTA_ID = None  # 2 daca e EUR
        if (self.currency_id.id != 29):
            BXVALUTA_ID = 2  # la factura 4808 cu un curs ; 2 EURO ; 1 RON
        else:
            BXVALUTA_ID = 1
        # verifica daca numarulFacturii exista
        BXIESIRE_ID = self.AvemNumarulFacturiiDeja(cur, numarFactura)
        if (not(BXIESIRE_ID>0)):
            self.adaugaFacturainEDA(cur, con, numarFactura, serieFactura, BXCONT_ID, BXREC_TYPE, BXVALUTA_ID,BXVALUTA_CURS)
            BXIESIRE_ID = self.AvemNumarulFacturiiDeja(cur, numarFactura)
            #AICI LUCRAM TODO1

        liniiFactura = self.env['account.invoice.line'].search([('invoice_id', '=', self.id)])
        BXIESIRELNSTable = Table("BXIESIRELNS", metadataEDA, autoload=True, autoload_with=engineEDA)
        for linieFactura in liniiFactura:
            _logger.info('Vedem daca merge')
            _logger.info("Inregistrari {0}".format(linieFactura.product_id.product_tmpl_id.default_code))
            ProdusSelectatEDA = ProdusEDA(linieFactura.product_id.product_tmpl_id.default_code)

            select_stmt = BXIESIRELNSTable.select().order_by(BXIESIRELNSTable.c.bxid.desc()).limit(1)
            command = engineEDA.execute(select_stmt).fetchone()
            LastInsertedID = command[0]
            newBXIDIesireLNS = LastInsertedID + 1  # adaugam 1
            BXLNS_TYPE = 1  # ptt Dragos ; 2 pentru SM
            # TODO - 03.03.2019- ce e cu BXLNS_TYPE
            isInline = False
            BXNET_AMOUNT = linieFactura.price_subtotal
            BXTVA_AMOUNT = linieFactura.price_total - BXNET_AMOUNT
            #linieFactura.
            #swanTVAIDA
            # boul de postgres converteste coloanele la small names
            insert_stmt = BXIESIRELNSTable.insert(None, isInline).values(bxid=newBXIDIesireLNS, bxrec_type=BXREC_TYPE, bxlns_type=BXLNS_TYPE, bxpart_id=ProdusSelectatEDA.EDA_BXID, bxcantitate=linieFactura.quantity, bxvaluta_id=BXVALUTA_ID,  bxlprice=linieFactura.price_unit, bxgprice=linieFactura.price_unit,  bxvat_id=ProdusSelectatEDA.EDA_BXCOTATVAIMPLICIT_ID,  bxnet_amount=BXNET_AMOUNT, bxtva_amount=round(BXTVA_AMOUNT,2),  bxtotal_amount=linieFactura.price_total,  bxnetl_amount=BXNET_AMOUNT, bxtval_amount=round(BXTVA_AMOUNT,2),  bxiesire_id=BXIESIRE_ID, bxcont_id=BXCONT_ID,  bxum_id=ProdusSelectatEDA.EDA_BXUM_ID, bxcomanda_id=None, bxcontgest_id=BXCONTGEST_ID)
            _logger.info(str(insert_stmt))
            rezultat = engineEDA.execute(insert_stmt)
        TblcountTable = Table("tblcount", metadataEDA, autoload=True, autoload_with=engineEDA)
        update_stmt = TblcountTable.update().values(lastid=newBXIDIesireLNS).where(
            TblcountTable.c.name == 'BXIESIRELNS')
        command = engineEDA.execute(update_stmt)
        _logger.info('Calculez totalul din dosarul : ' + str(self.dosar_id))
        facturat = sum(item.price_subtotal for item in liniiFactura)
        _logger.info('Total factura: ' + str(facturat))
        self.esteSincronizatEDA = True
        self.swanFacturaID = BXIESIRE_ID
        return  # iese din functie si asta e



        #### CAUTAM PRODUSELE SA LE ADAUGAM IN LISTA


        return


    def AvemNumarulFacturiiDeja(self, cur, numarFactura):
        interogare = "SELECT BXID FROM BXIESIRE WHERE BXDOC_NO LIKE \'" + str(numarFactura) + "\'"
        _logger.info(interogare)
        cur.execute(interogare)
        result = cur.fetchall()
        if (len(result) ==1 ):
          #  raise UserError("Factura "+str(numarFactura)+" este sincronizata")
            #trimite pentru procesare !
           # self.esteSincronizatEDA=True
            return result[0][0]
        elif (len(result) > 1):
            raise UserError("Exista mai multe inregistrari cu numarul de factura. Sincronizati manual ")
            return 0
        return 0


class ResPartner(models.Model):
    _inherit = 'res.partner'
    swan_ID = fields.Integer(string="ID din EDA")
    esteSincronizatEDA = fields.Boolean(string="Este sincronizat deja?")

    @api.one
    def sincronizeazaEDA(self, context=None):
        res = {}
        update = False
        if (self.esteSincronizatEDA == True):
            _logger.info('Baza de date este sincronizata')
            res = {'warning': {'title': _('Warning'), 'message': _('Este deja sincronizat' + str(self.name))}}
            return {
                'warning': {'title': _('Error'), 'message': _('Error message'), },
            }
        if res:
            return res
        if(self.parent_id.esteSincronizatEDA==True):
            _logger.info('Parintele '+str(self.parent_id)+' e sincronizat:')
            self.swan_ID=self.parent_id.swan_ID
            self.esteSincronizatEDA = True

        con = fdb.connect(
            host='192.168.2.163', database='D:\Contabilitate\DataBase\helpan.FDB',
            user='sysdba', password='masterkey'
        )
        cur = con.cursor()
        _logger.info("Verificam daca avem inregistrari\n");
        # TermenCautat=self.display_name.upper().replace("SC ","").replace(" SRL","").replace(" SA","")
        # csa caute si dupa CUI BXCODFISCAL=
        codCUI = self.vat.replace("CUI ", "").replace("RO ", "").replace("RO", "").replace(" ", "").strip()
        if (codCUI == ""):
            raise UserError(_('Nu avem CUIul setat la acest client \n '))
            return
        interogare = "SELECT bxid FROM BXCUSTOMER WHERE BXCODFISCAL='" + str(codCUI) + "'"
        _logger.info(interogare)
        cur.execute(interogare)

        result = cur.fetchall()
        if (len(result) == 1):
            newId = result[0][0]
            update = True
        else:
            if (len(result) > 1):
                raise UserError(
                    _('Prea multe rezultate pentru acest client \n Sunt ' + str(len(result)) + ' rezultate'))
                return
            else:
                cur.execute("select lastid from tblcount where name='BXCUSTOMER'")
                result = cur.fetchone()
                newId = result[0] + 1

        # TODO1 : verifica daca nu este deja

        _logger.info(str(self.display_name).encode('utf-8'))
        if (update == True):
            _logger.info('Actualizam date!')
            _logger.info("UPDATE BXCUSTOMER SET BXDENUMIRE='" + str(self.display_name) + "', BXCODFISCAL='" + str(
                self.vat) + "', BXREGCOM='" + str(self.nrc) + "',BXADRESA='" + str(self.street) + "', BXORAS='" + str(
                self.city) + "', BXEMAIL='" + str(self.email) + "' WHERE BXID="+str(newId))
            con.commit()
        else:
            _logger.info(
                "INSERT INTO BXCUSTOMER(BXID, BXDENUMIRE, BXCODFISCAL, BXREGCOM,BXADRESA, BXORAS, BXEMAIL,BXSERIA, BXINOUT_BOOL,BXSALARIAT_BOOL,BXGRUPACLIENTI_ID) VALUES(" + str(
                    newId) + ",'" + str(self.display_name) + "','" + str(self.vat) + "','" + str(
                    self.nrc) + "','" + str(self.street) + "','" + str(self.city) + "','" + str(
                    self.email) + "','RO',1,0,1)")
            cur.execute(
                "INSERT INTO BXCUSTOMER(BXID, BXDENUMIRE, BXCODFISCAL, BXREGCOM,BXADRESA, BXORAS, BXEMAIL,BXSERIA, BXINOUT_BOOL,BXSALARIAT_BOOL,BXGRUPACLIENTI_ID) VALUES(" + str(
                    newId) + ",'" + str(self.display_name) + "','" + str(self.vat) + "','" + str(
                    self.nrc) + "','" + str(self.street) + "','" + str(self.city) + "','" + str(
                    self.email) + "','RO',1,0,1)")
            _logger.info('\n\nID alocat: ' + str(newId) + ' - Incercam sa inseram in BXCUSTOMER\n\n')
            cur.execute("update tblcount set lastid=" + str(newId) + "  WHERE name='BXCUSTOMER'")
            con.commit()
        self.swan_ID = newId
        self.esteSincronizatEDA = True

    @api.one
    def sincronizeaza_eda(self, cr, uid, ids, context=None):
        return {
            'name': 'My Window',
            'domain': [],
            'res_model': 'res.partner',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {},
            'target': 'new',
        }


class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'
    dosar_id = fields.Many2one('dosar', 'Dosar')


class account_tax(models.Model):
    _inherit = 'account.tax'
    swanTVAID = fields.Integer(string="Inregistrare TVA in EDA")


class account_account(models.Model):
    _inherit = 'account.account'
    swanContID = fields.Integer(string="Identificator Cont in EDA",
                                help="Se deschide in SWAN in Setup->Conturi->Browse si se gaseste in coloana ID")


class crm_team(models.Model):
    _inherit = 'crm.team'
    ContFacturi = fields.Many2one('account.account', string='Cont alocat facturilor acestei echipe',
                                  help="Pentru Sincronizare cu EDA")
