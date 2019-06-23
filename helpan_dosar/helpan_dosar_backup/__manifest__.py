# -*- coding: utf-8 -*-
{
    'name': "helpan_dosar",

    'summary': """
        Afisare dosare ale lui helpan XXX - sincronizare cu serverul de web""",

    'description': """
       Afurisit el de manifest

       Relation from purchase order lines and invoice lines
    """,

    'author': "Helpan",
    'website': "http://www.helpan.ro",

    # for the full list
    'category': 'Helpan',
    'version': '0.44',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'purchase', 'account'],

    # always loaded
    'data': [
        'security/helpan_security.xml',
        'security/ir.model.access.csv',
        'views/helpan_dosar_view.xml',
        'views/inherited_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}