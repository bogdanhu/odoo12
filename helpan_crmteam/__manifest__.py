# -*- coding: utf-8 -*-
{
    'name': "helpan_crmteam",

    'summary': """
      WTF  Afisare produse conform echipei de vanzari""",

    'description': """
        In cadrul ofertelor (sale.order) cand se cauta in produse, se vor afisa doar produsele care apartin echipei de vanzari principale ale utilizatorului
    """,

    'author': "Helpan",
    'website': "http://www.helpan.ro",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.12',

    # any module necessary for this one to work correctly
    'depends': ['base','product','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}