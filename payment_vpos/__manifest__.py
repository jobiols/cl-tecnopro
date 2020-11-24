# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bancard vPOS Payment Acquirer',
    'category': 'Accounting/Payment Acquirers',
    'author': "Tecnopro",
    'website': 'https://tecnopro.com.py',
    'sequence': 375,
    'summary': 'Payment Acquirer: vPOS Implementation',
    'depends': ['payment', 'website'],
    'data': [
        'views/payment_vpos_templates.xml',
        'data/payment_acquirer_data.xml',
        'views/payment_views.xml',
        'data/process_id_sequence.xml'
    ],
    'application': True,
    'installable': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
    'uninstall_hook': 'uninstall_hook',
}
