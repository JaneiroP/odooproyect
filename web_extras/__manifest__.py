# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'web_extras',
    'category': 'Hidden',
    'version': '1.0',
    'description': """
Odoo Web core module.
========================

This module provides the core of the Odoo Web Client.
""",
    'depends': ['base','web'],
    'auto_install': True,
    'data': [
    ],
'assets': {
        'web.assets_common': [
            '/web_extras/static/src/js/MyControl.js',
            '/web_extras/static/src/js/search_bar.js'
        ],
},
    'bootstrap': True,  # load translations for login screen,
    'license': 'LGPL-3',
}
