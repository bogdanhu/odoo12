# -*- coding: utf-8 -*-
{
    'name': "helpan_dosar",

    'summary': """
        Afisare dosare ale lui helpan Daedalus- sincronizare cu serverul de web""",

    'description': """
      Adauga conceptul de dosar in Odoo- Urmeaza portarea din Daedalus

       Relation from purchase order lines and invoice lines      + res partner
       Am adaugat res.partner in lista
       Res.Currency
    """,

    'author': "Bogdan Hurezeanu",
    'website': "http://www.helpan.ro",

    # for the full list
    'category': 'Helpan',
    'version': '0.66',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'purchase', 'account', 'base_geolocalize','hr','mail','stock','delivery', 'sale_stock'],

    # always loaded
    'data': [
        'views/helpan_dosar_view.xml',
        'views/inherited_view.xml',
        'security/helpan_security.xml',
        'security/ir.model.access.csv',
    ],
    'images' : ['static/description/helpan.png'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
