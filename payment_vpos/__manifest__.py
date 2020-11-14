# -*- coding: utf-8 -*-

{
    'name': 'Bancard vPOS Payment Acquirer',
    'category': 'Accounting/Payment Acquirers',
    'author': "Tecnopro",
    'website': 'https://tecnopro.com.py',
    'sequence': 375,
    'summary': 'Payment Acquirer: vPOS Implementation',
    'depends': ['payment'],
    'data': [
        'data/payment_acquirer_data.xml',
        'views/payment_views.xml',
        'views/payment_bancard_templates.xml',
    ],
    'installable': True,
    'application': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
    'uninstall_hook': 'uninstall_hook',
}
