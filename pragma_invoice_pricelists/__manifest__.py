# -*- coding: utf-8 -*-
{
    "name": "HELPAN Invoice Pricelist",
    "version": "11.0.0.1.4",
    'license': 'OPL-1',
    'author': 'Josef Kaser, pragmasoft',
    'website': 'https://www.pragmasoft.de',
    'support': 'info@pragmasoft.de',
    'price': '19',
    'currency': 'EUR',
    "summary": """
    Set pricelist on customer invoice. Modificat de bogdan
    """,
    "description": """
Invoice Pricelist
=================
Bogdan Set a pricelist on the customer invoice. Recalculates the line item prices and sets the invoice currency when the pricelist is changed.
    """,
    "images": [
        "images/main_screenshot.png",
    ],
    "category": "Accounting",
    "depends": [
        "base",
        "account",
        "helpan_dosar",
    ],
    "data": [
        "views/invoice.xml",
    ],
    "installable": True,
    "auto_install": False,
}
