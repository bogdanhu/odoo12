# -*- coding: utf-8 -*-
{
    'name': "helpan_kiosk",

    'summary': """
        Afisare informatii legate de Dosare pe un TV
        Informatia va fi disponibila pe un site specific""",

    'description': """
        Modulul are rolul de a oferi o pagina dinamica prin care se afiseaza statusul dosarelor , respectiv ce joburi sunt pe workcenter
    """,

    'author': "Helpan",
    'website': "http://www.helpan.ro",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','helpan_dosar','website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        'views/example_webpage.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}